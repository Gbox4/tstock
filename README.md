# tstock - Generate stock charts in the terminal! 🚀🚀🚀

[![Downloads](https://pepy.tech/badge/tstock)](https://pepy.tech/project/tstock)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Gbox4/tstock?label=size)
![PyPI](https://img.shields.io/pypi/v/tstock)

📈 tstock is a tool to easily generate stock charts from the command line.

Just type `tstock aapl` to get a 3 month candlestick chart of $AAPL in your terminal!

<p align="center">
  <img src="https://github.com/Gbox4/Gbox4/raw/master/tstock-demo.gif" alt="tstock-demo">
</p>

# Features
- Stocks for most global exchanges
- Support for major cryptocurrencies
- Forex markets and currency exchange rates
- Different time intervals, including intraday trading
- "Wisdom"?!

# Dependencies

- Python 3.6 or greater
- Docker, if using the Docker version

# Installation

### AUR

`tstock` is available on the AUR. If you are on an Archlinux system, you can just install it using your AUR helper. Example using `yay`:

```
yay -S tstock
```

### PyPI

`tstock` is also available as a Python package. You can install it using `pip`:

```
pip install tstock
```

### Docker

1. Build Docker: `docker build -t tstock .`
2. Run: `docker run -e ALPHAVANTAGE_API_KEY=<yourkey> -it tstock:latest tstock aapl`

# Getting started

### AlphaVantage API setup

After installing `tstock`, you will need a AlphaVantage API key to pull the market data.

- Make a free AlphaVantage API account at https://www.alphavantage.co/support/#api-key
- After creating the account, you will see your free API key
- Run `export ALPHAVANTAGE_API_KEY=<your access key>`. You can make this permanent by adding this line to your .bashrc

### Usage

```
tstock --help
usage: tstock [-h] [-t INTERVAL] [-b COUNT] [-w] [-s] [--chart]
                   [-c CURRENCY] [-y LINES] [-a CLASS] [--padx COLUMNS]
                   [--pady LINES] [-v] [--version]
                   [TICKER]

tstock - generate stock charts in the terminal.

positional arguments:
  TICKER          Which ticker's data to pull.

options:
  -h, --help      show this help message and exit
  -t INTERVAL     Time interval of each candlestick. Valid values are '1min', '5min', '15min', '30min', '60min', 'day', 'week', or 'month'. Defaults to 'day'.
  -b COUNT        Number of time intervals back to go back. The number of candlesticks generated. Defaults to 70.
  -w              Enables extra words of 'wisdom'.
  -s              Short output, prints the last price only.
  --chart         Print the chart only. Overrides -w.
  -c CURRENCY     Set the currency. Only works with '-a crypto'. Defaults to 'USD'.
  -y LINES        Height of the chart. Defaults to 40.
  -a CLASS        The asset class of TICKER. Valid values are 'stock', 'crypto', and 'forex'. Autodetects depending on input ticker.
  --padx COLUMNS  Horizontal padding of the chart. Defaults to 5.
  --pady LINES    Vertical padding of the chart. Defaults to 4.
  -v              Toggle verbosity.
  --version       Print tstock version.

Examples:
    tstock aapl # chart of $AAPL
    tstock aapl -t 1min # the past 70 1-minute-intervals of $AAPL
    tstock aapl -t 60min -b 24 # the past 24 60-minute-intervals (aka past day) of $AAPL
    tstock aapl -t 60min -b 24 -y 20 # same as above, but only 20 lines high
    tstock btc # chart of the cryptocurrency $BTC
    tstock btc -w # same as above, with rocket ships 🚀🚀🚀
    tstock btc -c GBP # same as above, but in currency GBP
    tstock usd/eur # chart of the price of USD in euros
```

Run `tstock TICKER` to get the 70 day chart of `$TICKER`. Use `-b COUNT` to specify the number of intervals back you want to pull. `-t INTERVAL` will specify the time interval of each candlestick. Use `-y LINES` to specify the length of the chart's y axis.

To get cryptocurrencies, use the `-a crypto` option. For example, `tstock -a crypto BTC` would fetch a price chart of Bitcoin.

For more options, run `tstock -h`

You can get international markets by specifying a code after `.`. For example, to get SAIC Motor Corporation on the Shanghai Stock Exchange, run `tstock 600104.SHH`. Find more information on how to specify special tickers on AlphaVantage's docs: https://www.alphavantage.co/documentation

# Notes

- The free tier of the API is limited to 500 API calls per day, 5 calls per minute.
- If you are using Windows, the ANSI escape codes will not display properly in the default cmd shell or PowerShell. Please use a terminal emulator that supports ANSI escape codes such as <a href='https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab'>Windows Terminal</a>.

# Donate

I develop `tstock` for free in my spare time. If you like it, and want to buy me a coffee, I'd really appreciate it.

Donate: https://www.buymeacoffee.com/Gbox4

Bitcoin: (<a href='https://i.ibb.co/b2rS0kV/btcgithubtstock.png'>QR</a>) `bc1qusuztegpfuh7jk25l2dx5xyjvasgryrqg42d5n`

BCH: (<a href='https://i.ibb.co/WpWv96K/download.png'>QR</a>) `qq0gedhne30lcr3253zz08sy4ryxukgx4gcrk6qzjg`

Monero: (<a href='https://i.ibb.co/PNhgC3q/xmrgithubtstock.png'>QR</a>) `87wuCKbbchKV8Dz3JRoSN3jaqWBSiEShFXkFrYUaKT8Bew4P7dFvUJWVVR6RLr84J44QCdtNVyR6QC7aCSKYUWfnGK9y4K2`

Nano: `nano_15pqkfph8wfk4dbtkcrq88giff6xgqzs3znf44nfe1g8sgaixwaj6pbepsmn`
