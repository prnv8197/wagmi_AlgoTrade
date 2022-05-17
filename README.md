# wagmi_AlgoTrade_ver1

Crypto trading model
wagmi_Strategy.py file contains a single function that return a string 'Long' if trade taken is a long trade and 'Short' if the trade to be taken is a short trade, else it return 'Pass' to move to next iteration.
Params:

crypto_asset : Tickr of the asset; default = 'USD-BTC'

p_interval : Interval size of primary candle; default = '15m'

p_period : Period of primary candle data; default = '1mo'

s_interval : Interval size of secondary candle; default = '5m'

s_period : Period of secondary candle data; default = '1mo'

# Run the freqtrade bot

YOu need docker installed!

```
docker-compose pull
docker-compose up -d
```

# Run backtesting

```
# Download historical data first
docker-compose run --rm freqtrade download-data --exchange binance

# Run backtesting using your strategy
docker-compose run --rm freqtrade backtesting --config user_data/config.json --strategy Zeno --dry-run-wallet 1100
```
