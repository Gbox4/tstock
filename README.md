# tstock - Check stocks from the terminal!

📈 tstock is a tool to easily generate stock charts from the command line.

Just type `tstock aapl` to get a 3 month candlestick chart of $AAPL in your terminal!

<img src="https://i.ibb.co/x7xB8w6/tstock2-0-5.png" alt="tstockex" border="0">

# Features
- Stocks for most global exchanges
- Support for major cryptocurrencies
- Different time intervals, including intraday trading
- "Wisdom"?!

# Dependencies

- Python 3.6 or greater

# Installation

### AUR

`tstock` is available on the AUR. If you are on an Archlinux system, you can just install it using your AUR helper. Example using `yay`:

```
yay -S tstock
```

### PyPI

`tstock` is also available as a Python package. You can install it using `pip`:

```
pip3 install tstock
```

# Getting started

### AlphaVantage API setup

After installing `tstock`, you will need a AlphaVantage API key to pull the market data.

- Make a free AlphaVantage API account at https://www.alphavantage.co/support/#api-key
- After creating the account, you will see your free API key
- Run `export ALPHAVANTAGE_API_KEY=<your access key>`. You can make this permanent by adding this line to your .bashrc

### Usage

Run `tstock TICKER` to get the 70 day chart of `$TICKER`. Use `-b COUNT` to specify the number of days back you want to pull. `-t INTERVAL` will specify the time interval of each candlestick. Use `-y LINES` to specify the length of the chart's y axis.

To get cryptocurrencies, use the `-a crypto` option. For example, `tstock -a crypto BTC` would fetch a price chart of Bitcoin.

You can get international markets by specifying a code after `.`. For example, to get SAIC Motor Corporation on the Shanghai Stock Exchange, run `tstock 600104.SHH`. Find more information on how to specify special tickers on AlphaVantage's docs: https://www.alphavantage.co/documentation

# Notes

- The free tier of the API is limited to 500 API calls per day, 5 calls per minute.
