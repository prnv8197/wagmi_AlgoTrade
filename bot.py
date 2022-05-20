#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import dydx3.constants as consts
from sympy import false, true

from strategies.zeno import ZenoStrategy
from utils.dydx import setup_dydx


process_throttle_secs = 5


def go_long(dydx_client, amount, stop_loss, roi):
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
    market_buy_order = dydx_client.private.create_order(**order_params).data
    # TODO: Might need to check here if order filled or not!
    print(market_buy_order)

    buy_price = market_buy_order['order']['price']

    # Also make a stop loss order
    stoploss_order = client.private.create_order(
        position_id=position_id,
        market=consts.MARKET_ETH_USD,
        side=consts.ORDER_SIDE_SELL,
        order_type=consts.ORDER_TYPE_TRAILING_STOP,
        post_only=False,
        size=str(amount),
        price="1",  # Dunno what to do here
        trailing_percent='-%f' % stop_loss,  # NEed to switch back to triggerPrice
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 15000,
    ).data
    print(stoploss_order)

    take_profit_price = '%.1f' % (float(buy_price) * (1 + (roi/100)))
    trigger_profit_price = '%.1f' % (float(buy_price) * (1 + (roi/200)))
    # Also make a take-profit order
    take_profit_order = client.private.create_order(
        position_id=position_id,
        market=consts.MARKET_ETH_USD,
        side=consts.ORDER_SIDE_SELL,
        order_type=consts.ORDER_TYPE_TAKE_PROFIT,
        post_only=False,
        size=str(amount),
        price=take_profit_price,
        trigger_price=trigger_profit_price,
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 15000,
    ).data
    print(take_profit_order)

    return {
        "market_buy_order": market_buy_order,
        "stop_loss_order": stoploss_order,
        "take_profit_order": take_profit_order
    }


def check_if_pending(orders, dydx_client):
    # GEt current active orders
    # If none, return false
    # Else check for a buy order
    # if there, check status
    if orders == {}:
        print("No active orders!")
        return False
    # MAke sure the market buy order is not cancelled
    market_buy_order = dydx_client.private.get_order_by_id(
        orders['market_buy_order']['order']['id']).data
    # Else, clear out orders
    order_status = market_buy_order['order']['status']

    # If pending, return true
    if (order_status == consts.ORDER_STATUS_PENDING):
        print("buy order pending!")
        return True
    # If filled, check stop orders
    elif (order_status == consts.ORDER_STATUS_FILLED):
        print("buy order filled!")
        # Check if we've taken stop loss or profit
        stop_loss_order = dydx_client.private.get_order_by_id(
            orders['stop_loss_order']['order']['id']).data
        if stop_loss_order['order']['status'] == consts.ORDER_STATUS_FILLED:
            print("Target reached! Ready for new orders")
            # if we have, cancel the other order and return false
            dydx_client.private.cancel_order(
                order_id=orders['take_profit_order']['order']['id'])
            orders = {}
            return false

        take_profit_order = dydx_client.private.get_order_by_id(
            orders['take_profit_order']['order']['id']).data
        if take_profit_order['order']['status'] == consts.ORDER_STATUS_FILLED:
            print("Target reached! Ready for new orders")
            # if we have, cancel the other order and return false
            dydx_client.private.cancel_order(
                order_id=orders['stop_loss_order']['order']['id'])
            orders = {}
            return false

        if stop_loss_order['order']['status'] == consts.ORDER_STATUS_CANCELED or take_profit_order['order']['status'] == consts.ORDER_STATUS_CANCELED:
            print("One of the target orders canceled Ready for new orders")
            # clear out remaining sell orders
            try:
                dydx_client.private.cancel_order(
                    order_id=orders['stop_loss_order']['order']['id'])
                dydx_client.private.cancel_order(
                    order_id=orders['take_profit_order']['order']['id'])
                # clear out the long position too
                dydx_client.private.cancel_order(
                    order_id=orders['market_buy_order']['order']['id'])
            except:
                print("One order was already canceled")
            # Reset current_orders
            orders = {}
            return False
        # IF we haven't, keep waiting return true
        print("Waiting on profit/loss target")
        return True
    else:
        print("Buy order not fulfilled. Ready for new orders!")
        # clear out remaining sell orders
        dydx_client.private.cancel_order(
            order_id=orders['stop_loss_order']['order']['id'])
        dydx_client.private.cancel_order(
            order_id=orders['take_profit_order']['order']['id'])
        # Reset current_orders
        orders = {}
        return False

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


def start_bot(dydx_client, strategy):
    current_orders = {}
    while(True):
        # Run the strat every x seconds
        time.sleep(process_throttle_secs)

        # If there pending open orders, no trades will be placed
        if check_if_pending(current_orders, dydx_client):
            continue

        # Run our strategy
        if (strategy.should_long()):
            current_orders = go_long(
                dydx_client, amount=0.01, stop_loss=1, roi=1)

if __name__ == "__main__":
    client = setup_dydx()
    strat = ZenoStrategy(client, consts.MARKET_ETH_USD)
    start_bot(client, strat)
