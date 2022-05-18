#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent.futures import process
import time
from strategies import MyStrategy1

process_throttle_secs = 5

if __name__ == "__main__":
    while(True):
        print(MyStrategy1())
        time.sleep(process_throttle_secs)
