#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from dydx3 import Client
import dydx3.constants as consts
from dydx3 import private_key_to_public_key_pair_hex
from web3 import Web3
import os
from dotenv import load_dotenv

from strategies import MyStrategy1


load_dotenv()

process_throttle_secs = 5


def setup_dydx():
    # My Account 2 metamask address
    ETHEREUM_ADDRESS = '0x17C562B0E8Fa75354C1b45F4f5dD8a2b6f38d663'
    # Using Etthereum node hosted on ChainStack.
    WEB_PROVIDER_URL = os.getenv('WEB_PROVIDER_URL')

    client = Client(
        network_id=consts.NETWORK_ID_ROPSTEN,
        host=consts.API_HOST_ROPSTEN,
        default_ethereum_address=ETHEREUM_ADDRESS,
        web3=Web3(Web3.HTTPProvider(WEB_PROVIDER_URL)),
        eth_private_key=os.getenv('ETH_PRIVATE_KEY')
    )

    # Set STARK key.
    stark_private_key = client.onboarding.derive_stark_key()
    client.stark_private_key = stark_private_key

    return client


def go_long(dydx_client, amount, stop_loss):
    # Get our position ID.
    account_response = dydx_client.private.get_account()
    position_id = account_response.data['account']['positionId']

    eth_market = client.public.get_markets(market=consts.MARKET_ETH_USD)
    buy_price = eth_market.data['markets']['ETH-USD']['oraclePrice']

    # Make a market buy order
    order_params = {
        'position_id': position_id,
        'market': consts.MARKET_ETH_USD,
        'side': consts.ORDER_SIDE_BUY,
        'order_type': consts.ORDER_TYPE_MARKET,
        'post_only': False,
        'size': str(amount),
        'price': '%.1f' % float(buy_price),  # Set prceision to tick_size 0.1
        'limit_fee': '0.0015',
        'expiration_epoch_seconds': time.time() + 15000,
        'time_in_force': consts.TIME_IN_FORCE_IOC
    }
    order_response = dydx_client.private.create_order(**order_params)
    # TODO: Might need to check here if order filled or not!
    print(order_response.data)

    buy_price = order_response.data['order']['price']
    stop_trigger_price = '%.1f' % (float(buy_price) * (1-stop_loss))
    stop_limit_price = '%.1f' % (float(buy_price) * (1-stop_loss*5))

    # Also make a stop loss order
    stoploss_order = client.private.create_order(
        position_id=position_id,
        market=consts.MARKET_ETH_USD,
        side=consts.ORDER_SIDE_SELL,
        order_type=consts.ORDER_TYPE_TRAILING_STOP,
        post_only=False,
        size=str(amount),
        price="1", # Dunno what to do here
        trailing_percent='-%f' % stop_loss,
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 15000,
    )
    print(stoploss_order.data)

    # Also make a take-profit order

    return order_response


def check_open_orders(dydx_client):
    # Count open orders (there should be exactly one).
    orders_response = dydx_client.private.get_orders(
        market=consts.MARKET_ETH_USD,
        status=consts.ORDER_STATUS_OPEN,
    )
    print(orders_response.data)
    return len(orders_response.data['orders']) > 0

# def go_short(dydx_client):
#     # Get our position ID.
#     account_response = dydx_client.private.get_account()
#     position_id = account_response['data']['account']['positionId']
#     order_params = {
#                 'position_id': position_id,
#                 'market': consts.MARKET_ETH_USD,
#                 'side': consts.ORDER_SIDE_BUY,
#                 'order_type': consts.ORDER_TYPE_MARKET,
#                 'post_only': False,
#                 'size': '0.0001',
#                 # 'price': '20',
#                 'limit_fee': '0.0015',
#                 'expiration_epoch_seconds': time.time() + 15000,
#                 }
#     order_response = dydx_client.private.create_order(**order_params)
#     return order_response


def start_bot(dydx_client):
    while(True):
        # Run the strat every x seconds
        time.sleep(process_throttle_secs)

        # Check for open orders and skip this loop if there is one
        if check_open_orders(dydx_client):
            continue
        if (MyStrategy1() == "Long"):
            print("Go long")
            print(go_long(dydx_client, 0.0001, 0.01))
        elif(MyStrategy1() == "Short"):
            print("short!")
        else:
            print("Pass")


if __name__ == "__main__":
    client = setup_dydx()
    # start_bot(client)
    go_long(client, 0.01, 1)
