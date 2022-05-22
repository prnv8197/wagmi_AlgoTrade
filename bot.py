#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import dydx3.constants as consts
from sympy import false, true

from strategies.zeno import ZenoStrategy
from utils.dydx import setup_dydx, go_long, check_if_pending


process_throttle_secs = 30

def start_bot(dydx_client, strategy):
    current_orders = {}
    while(True):
        # Run the strat every x seconds
        time.sleep(process_throttle_secs)

        # If there pending open orders, no trades will be placed
        if check_if_pending(current_orders, dydx_client):
            continue
        # We can reset order here
        current_orders = {}

        # Run our strategy
        if (strategy.should_long()):
            current_orders = go_long(
                dydx_client, amount=3.5, stop_loss=1, roi=1)

if __name__ == "__main__":
    client = setup_dydx()
    strat = ZenoStrategy(client, consts.MARKET_ETH_USD)
    start_bot(client, strat)
