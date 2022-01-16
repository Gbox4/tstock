import os
import argparse
import datetime
import random
import requests
import numpy as np

VERSION = "2.0.0"


def translate(x, l1, h1, l2, h2):
    """Translate from one range to another.
    
    Arguments:
        x (number) - number to translate in range 1.
        l1 (number) - lower bound of range 1.
        h1 (number) - upper bound of range 1.
        l2 (number) - lower bound of range 2.
        h2 (number) - upper bound of range 2.

    Returns:
        y (number) - x mapped to range 2.
    """
    return (((x - l1) / (h1 - l1)) * (h2 - l2)) + l2


def get_api_key():
    """Gets the API key from the environment variable MARKETSTACK_API_KEY, raises an error if not found."""
    if not 'MARKETSTACK_API_KEY' in list(os.environ.keys()):
        print("error: API key not detected! Follow these instructions to get your API Key working:\n" + \
        "- Make a free MarketStack API account at https://marketstack.com/signup/free\n" + \
        "- Login and find your API Access Key on the Dashboard page\n" + \
        "- Run \"export MARKETSTACK_API_KEY=<your access key>\"." + \
        "You can make this permanent by adding this line to your .bashrc\n")
        exit(1)
    return os.environ['MARKETSTACK_API_KEY']


def main():
    """Main tstock script body."""

    parser = get_args()
    parse_args_exit(parser)

    padX = 5  # TODO: make padX an option
    padY = 4
    days_back = 90
    verbose = False
    chart_only = False
    wisdom = False
    maxY = 40

    # Parse arguments
    args = parser.parse_args()
    ticker = args.ticker[0]
    if args.d:
        days_back = int(args.d)
    if args.v:
        verbose = args.v
    if args.y:
        maxY = args.y
    if args.c:
        chart_only = args.c
    if args.w:
        wisdom = args.w

    # HTTP GET API data
    apikey = get_api_key()
    date_to = datetime.datetime.today().strftime('%Y-%m-%d')
    date_from = (datetime.datetime.today() -
                 datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
    request_url = f'http://api.marketstack.com/v1/eod?access_key={apikey}&date_from={date_from}&date_to={date_to}&symbols={ticker}'

    if verbose:
        print(
            f"Days Back: {days_back}\nTicker: {ticker}\nAPI Key: {apikey}\nRequest URL: {request_url}\nY height: {maxY}"
        )

    r = requests.get(request_url).json()
    if 'error' in list(r.keys()):
        print(f"error: The API returned the following error:\n{r}")
        exit(1)
    data = r['data']

    # Parse API data
    candlesticks = []
    for d in data:
        candlesticks.append(
            (d['open'], d['high'], d['low'], d['close'], d['date'][8:10]))

    candlesticks = list(reversed(candlesticks))
    maxX = len(candlesticks) + padX * 2 + 2

    # Create the chart
    chart = np.array([[" " for x in range(maxX)] for y in range(maxY)])
    column_colors = ["\x1b[0m" for x in range(maxX)
                     ]  # Stores ANSI escape sequences for printing color
    # Draw borders
    chart[0, :] = "─"
    chart[-1, :] = "─"
    chart[:, 0] = "│"
    chart[:, -1] = "│"
    chart[0, 0] = "┌"
    chart[0, -1] = "┐"
    chart[-1, 0] = "└"
    chart[-1, -1] = "┘"
    # Draw graph title, if there are there enough worth of data to contain it
    title = f"┤  {days_back} Day Stock Price for ${ticker.upper()}  ├"
    if maxX >= len(title) + 2:
        for i, c in enumerate(title):
            chart[0, i + 1] = c
    # Find all time high and all time low
    ath = 0
    atl = 99999999
    for c in candlesticks:
        if c[1] > ath:
            ath = c[1]
        if c[2] < atl:
            atl = c[2]
    # Draw candlesticks
    start_i = 1 + padX
    end_i = maxX - 1 - padX
    y_axis_low = padY
    y_axis_high = maxY - padY
    for i, c in enumerate(candlesticks):
        shifted_i = i + start_i
        # Stuff gets a little confusing here because the graph has to be y-inverted. "high" is referring to a high price, but needs to be flipped to a low index.
        translated_open = int(
            translate(c[0], atl, ath, y_axis_high, y_axis_low))
        translated_high = int(
            translate(c[1], atl, ath, y_axis_high, y_axis_low))
        translated_low = int(translate(c[2], atl, ath, y_axis_high,
                                       y_axis_low))
        translated_close = int(
            translate(c[3], atl, ath, y_axis_high, y_axis_low))
        # Draw high/low
        for y in range(translated_high, translated_low + 1):
            chart[y, shifted_i] = "|"
        # Draw open/close
        # Positive day, stock went up
        if c[0] < c[3]:
            column_colors[shifted_i] = "\x1b[32m"  # ANSI green
            tmp = translated_low
            translated_low = translated_high
            translated_high = tmp
            for y in range(translated_close, translated_open + 1):
                chart[y, shifted_i] = "█"
        # Negative day, stock went down
        else:
            column_colors[shifted_i] = "\x1b[31m"  # ANSI red
            for y in range(translated_open, translated_close + 1):
                chart[y, shifted_i] = "█"

    # Setup x-axis labels
    x_axis_labels = " " * (1 + padX)
    for i in range(start_i, end_i):
        shifted_i = i - start_i
        if (shifted_i) % 5 == 0:
            chart[-1, i] = "┼"
            if int(candlesticks[shifted_i][4]) >= 10:
                x_axis_labels += f"{candlesticks[shifted_i][4]}   "
            else:
                x_axis_labels += f"{int(candlesticks[shifted_i][4])}    "
    x_axis_labels += " " * (maxX - len(x_axis_labels))

    # Setup y-axis labels
    y_axis_labels = []
    margin = len("${:,.2f}".format(ath))
    for i in range(maxY):
        if i >= y_axis_low and i <= y_axis_high:
            shifted_i = y_axis_high - i
            if shifted_i % 4 == 0:
                chart[i, 0] = "┼"
                label = "${:,.2f}".format(
                    translate(shifted_i, y_axis_low, y_axis_high, atl, ath))
                y_axis_labels.append(" " * (margin - len(label)) + f"{label}")
            else:
                y_axis_labels.append(" " * margin)
        else:
            y_axis_labels.append(" " * margin)

    # Print out the chart
    for y, row in enumerate(chart):
        out = ""
        out += y_axis_labels[y]
        for x, char in enumerate(row):
            if y >= y_axis_low and y <= y_axis_high:
                out += column_colors[x]
            out += char
        print(out)
    # Print x axis labels
    print(y_axis_labels[0] + x_axis_labels)
    print()

    if not chart_only:
        #Print additional info
        print("Last price:\t${:,.2f}".format(candlesticks[-1][3]))
        print(f"% change:\t{round(100*(candlesticks[-1][3]-candlesticks[0][0])/candlesticks[-1][3],2)}%")
        if wisdom:
            if candlesticks[-1][3] > candlesticks[0][0]:
                print(random.choice([
                    f"${ticker.upper()} to the moon! 🚀🚀🚀",
                    "Apes alone weak, apes together strong 🦍🦍🦍",
                    f"${ticker.upper()} primary bull thesis: I like the stock."
                    "Stocks can only go down 100% but can go up infinite %. Stocks can literally only go up. Q.E.D.",
                ]))
            else:
                print(random.choice([
                    "Losses aren't real 'till you sell 💎🙌",
                    "Literally cannot go tits up 💎🙌",
                    "GUH.",
                    "Short squeeze any time now 💎🙌"
                ]))
        print()

def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if args.version:
        parser.exit(0, f"tstock {VERSION}\n")


def get_args():
    """Get the script arguments."""
    description = "tstock - check stocks from the terminal"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("ticker",
                     metavar="TICKER",
                     nargs=1,
                     help="Specify which ticker's data to pull.")

    arg.add_argument(
        "-d",
        metavar="days", type=int,
        help="Number of days to go back in API call. Defaults to 90.")

    arg.add_argument("-y",
                     metavar="lines", type=int,
                     help="Specify height of the chart. Defaults to 40.")

    arg.add_argument("-v", action="store_true", help="Toggles verbosity.")
    arg.add_argument("-c", action="store_true", help="Prints the chart only. Overrides -w.")
    arg.add_argument("-w", action="store_true", help="Prints some extra words of 'wisdom'.")

    arg.add_argument("--version",
                     action="store_true",
                     help="Print tstock version.")

    return arg


if __name__ == "__main__":
    main()