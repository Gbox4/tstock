# tstock - Check stocks from the terminal!

📈 tstock is a tool to easily generate stock charts from the command line.

Just type `tstock aapl` to get a 3 month candlestick chart of $AAPL in your terminal!

Example:

<img src="https://i.ibb.co/Pry8DWC/tstockex.png" alt="tstockex" border="0">

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

### MarketStack API setup

After installing `tstock`, you will need a MarketStack API key to pull the market data.

- Make a free MarketStack API account at https://marketstack.com/signup/free
- Login and find your API Access Key on the Dashboard page
- Run `export MARKETSTACK_API_KEY=<your access key>`. You can make this permanent by adding that command to your `.bashrc`.

### Usage

Run `./tstock TICKER` to get the 3 month chart of `$TICKER`. Use `-d DAYS` to specify the number of days back you want to pull. Use `-y LINES` to specify the length of the chart's y axis.

You can get indexes by appending `.INDX`. for example, `./tstock DJI.INDX` to get the Dow Jones Industrial Average. Find more information on how to specify special tickers on MarketWatch's API Docs: https://marketstack.com/documentation

# Notes

- The free tier of the API is limited to 500 API calls per day, 5 calls per minute.
