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

    # Get dYdX account balances
    my_balances = client.private.get_account()
    print(my_balances.__dict__)


def start_bot():
    while(True):
        if (MyStrategy1() == "Long"):
            print("Go long")
        elif(MyStrategy1() == "Short"):
            print("short!")
        else:
            print("PAss")
        time.sleep(process_throttle_secs)


if __name__ == "__main__":
    setup_dydx()
