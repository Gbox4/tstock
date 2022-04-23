# Written by Gabe Banks 2022 <https://gabebanks.net>

__version__ = "2.2.6"

# Printed as a part of --help
extra_help = """Examples:
    tstock aapl # chart of $AAPL
    tstock aapl -b 24 -t 60min # the past 24 60-minute-intervals of $AAPL, 20 lines high
    tstock -s shopify # search the API for keyword "shopify"
    tstock shop.trt # chart of $SHOP on the TRT exchange
    tstock btc -c GBP -w # chart of the price of Bitcoin in GBP with rockets 
    tstock usd/eur # chart of the price of USD in euros
"""
