# Written by Gabe Banks 2022 <https://gabebanks.net>

__version__ = "2.2.3"

# Printed as a part of --help
extra_help = """Examples:
    tstock aapl # chart of $AAPL
    tstock aapl -t 1min # chart of 1-minute-intervals of $AAPL
    tstock aapl -t 60min -b 24 # the past 24 60-minute-intervals (aka past day) of $AAPL
    tstock aapl -t 60min -b 24 -y 20 # same as above, but only 20 lines high
    tstock btc # chart of the cryptocurrency $BTC
    tstock btc -w # same as above, with rocket ships
    tstock btc -c GBP # same as above, but in currency GBP
    tstock usd/eur # chart of the price of USD in euros
"""
