# Written by Gabe Banks 2022 <https://gabebanks.net>

__version__ = "2.1.1"

extra_help = """Examples:
    tstock aapl # chart of $AAPL
    tstock aapl -t 1min # the past 70 1-minute-intervals of $AAPL
    tstock aapl -t 60min -b 24 # the past 24 60-minute-intervals (aka past day) of $AAPL
    tstock aapl -t 60min -b 24 -y 20 # same as above, but only 20 lines high
    tstock btc -a crypto # chart of the cryptocurrency $BTC
    tstock btc -a crypto -c GBP # same as above, but in currency GBP
    tstock btc -a crypto -c EUR -s # print only the last price of $BTC in EUR
    tstock usd/eur -a forex # chart of the price of USD in euros
"""