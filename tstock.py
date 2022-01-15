#!/usr/bin/python

import os
import argparse
import datetime
from xmlrpc.client import MAXINT
import requests
import numpy as np

def translate(x, l1, h1, l2, h2):
    return (((x - l1) / (h1 - l1)) * (h2 - l2)) + l2

def get_api_key():
    if not 'MARKETSTACK_API_KEY' in list(os.environ.keys()):
        print("error: API key not detected! Follow these instructions to get your API Key working:\n" + \
        "- Make a free MarketStack API account at https://marketstack.com/signup/free\n" + \
        "- Login and find your API Access Key on the Dashboard page\n" + \
        "- Run \"export MARKETSTACK_API_KEY=<your access key>\"." + \
        "You can make this permanent by adding this line to your .bashrc\n")
        exit(1)
    return os.environ['MARKETSTACK_API_KEY']


def main():
    padX = 5 # TODO: make padX an option
    padY = 4
    days_back = 90
    ticker = "aapl"
    verbose = True
    maxY = 40

    # HTTP GET API data
    apikey = get_api_key()
    date_to = datetime.datetime.today().strftime('%Y-%m-%d')
    date_from = (datetime.datetime.today() -
                datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
    request_url = f'http://api.marketstack.com/v1/eod?access_key={apikey}&date_from={date_from}&date_to={date_to}&symbols={ticker}'

    if verbose:
        print(f"Days Back: {days_back}\nTicker: {ticker}\nAPI Key: {apikey}\nRequest URL: {request_url}")

    r = requests.get(request_url).json()
    if 'error' in list(r.keys()):
        print(f"error: The API returned the following error:\n{r}")
        exit(1)
    data = r['data']

    # Parse API data
    candlesticks = []
    for d in data:
        candlesticks.append((d['open'], d['high'], d['low'], d['close'], d['date'][8:10]))

    candlesticks = list(reversed(candlesticks))
    # candlesticks = list(reversed([(171.34, 173.78, 171.09, 173.07, '14'), (175.78, 176.62, 171.79, 172.19, '13'), (176.12, 177.179, 174.821, 175.53, '12'), (172.32, 175.18, 170.82, 175.08, '11'), (169.08, 172.5, 168.17, 172.19, '10'), (172.89, 174.14, 171.03, 172.17, '07'), (172.7, 175.3, 171.64, 172.0, '06'), (179.61, 180.17, 174.64, 174.92, '05'), (182.63, 182.9, 179.12, 179.7, '04'), (177.83, 182.88, 177.71, 182.01, '03'), (178.085, 179.23, 177.26, 177.57, '31'), (179.47, 180.57, 178.09, 178.2, '30'), (179.33, 180.63, 178.14, 179.38, '29'), (180.16, 181.33, 178.53, 179.29, '28'), (177.085, 180.42, 177.07, 180.33, '27'), (175.85, 176.85, 175.27, 176.28, '23'), (173.04, 175.86, 172.15, 175.64, '22'), (171.56, 173.2, 169.12, 172.99, '21'), (168.28, 170.58, 167.46, 169.75, '20'), (169.93, 173.47, 169.69, 171.14, '17'), (179.28, 181.14, 170.75, 172.26, '16'), (175.11, 179.5, 172.31, 179.3, '15'), (175.25, 177.74, 172.21, 174.33, '14'), (181.115, 182.09, 175.53, 175.74, '13'), (175.205, 179.63, 174.69, 179.45, '10'), (174.91, 176.75, 173.92, 174.56, '09'), (172.125, 175.95, 170.7, 175.08, '08'), (169.08, 171.58, 168.34, 171.18, '07'), (164.29, 167.8799, 164.28, 165.32, '06'), (164.02, 164.96, 159.72, 161.84, '03'), (158.74, 164.2, 157.8, 163.76, '02'), (167.48, 170.295, 164.53, 164.77, '01'), (159.99, 165.52, 159.92, 165.3, '30'), (159.37, 161.19, 158.7901, 160.24, '29'), (159.57, 160.45, 156.36, 156.81, '26'), (160.75, 162.14, 159.64, 161.94, '24'), (161.12, 161.8, 159.07, 161.41, '23'), (161.68, 165.7, 161.0, 161.02, '22'), (157.65, 161.02, 156.53, 160.55, '19'), (153.71, 158.67, 153.05, 157.87, '18'), (150.995, 155.0, 150.995, 153.49, '17'), (149.94, 151.49, 149.34, 151.0, '16'), (150.37, 151.88, 149.43, 150.0, '15'), (148.43, 150.4, 147.48, 149.99, '12'), (148.96, 149.43, 147.68, 147.87, '11'), (150.02, 150.1297, 147.85, 147.92, '10'), (150.2, 151.428, 150.07, 150.81, '09'), (151.41, 151.55, 150.16, 150.44, '08'), (151.89, 152.2, 150.06, 151.28, '05'), (151.58, 152.43, 150.64, 150.96, '04'), (150.39, 151.97, 149.83, 151.49, '03'), (148.66, 151.57, 148.65, 150.02, '02'), (148.985, 149.7, 147.8, 148.96, '01'), (147.22, 149.94, 146.41, 149.8, '29'), (149.82, 153.165, 149.72, 152.57, '28'), (149.36, 149.73, 148.49, 148.85, '27'), (149.33, 150.84, 149.01, 149.32, '26'), (148.68, 149.37, 147.6211, 148.64, '25'), (149.69, 150.18, 148.64, 148.69, '22'), (148.81, 149.64, 147.87, 149.48, '21'), (148.7, 149.7522, 148.12, 149.26, '20'), (147.01, 149.17, 146.55, 148.76, '19'), (143.445, 146.84, 143.16, 146.55, '18')]))
    maxX = len(candlesticks) + padX * 2 + 2


    # Create the chart
    chart = np.array([[" " for x in range(maxX)] for y in range(maxY)])
    column_colors = ["\x1b[0m" for x in range(maxX)] # Stores ANSI escape sequences for printing color
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
            chart[0, i+1] = c
    # Find all time high and all time low
    ath = 0
    atl = MAXINT
    for c in candlesticks:
        if c[1] > ath:
            ath = c[1]
        if c[2] < atl:
            atl = c[2]
    print(ath, atl)
    # Draw candlesticks
    start_i = 1 + padX
    end_i = maxX - 1 - padX
    y_axis_low = padY
    y_axis_high = maxY - padY
    print(y_axis_high)
    for i, c in enumerate(candlesticks):
        shifted_i = i+start_i
        # Stuff gets a little confusing here because the graph has to be y-inverted. "high" is referring to a high price, but needs to be flipped to a low index.
        translated_open = int(translate(c[0], atl, ath, y_axis_high, y_axis_low))
        translated_high = int(translate(c[1], atl, ath, y_axis_high, y_axis_low))
        translated_low = int(translate(c[2], atl, ath, y_axis_high, y_axis_low))
        translated_close = int(translate(c[3], atl, ath, y_axis_high, y_axis_low))
        # Draw high/low
        for y in range(translated_high, translated_low+1):
            chart[y, shifted_i] = "|"
        # Draw open/close
        # Positive day, stock went up
        if c[0] < c[3]:
            column_colors[shifted_i] = "\x1b[32m" # ANSI green
            tmp = translated_low
            translated_low = translated_high
            translated_high = tmp
            for y in range(translated_close, translated_open+1):
                chart[y, shifted_i] = "█"
        # Negative day, stock went down
        else:
            column_colors[shifted_i] = "\x1b[31m" # ANSI red
            for y in range(translated_open, translated_close+1):
                chart[y, shifted_i] = "█"

    # Setup x-axis labels
    x_axis_labels = " " * (1+padX)
    for i in range(start_i, end_i):
        shifted_i = i-start_i
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
                label = "${:,.2f}".format(translate(shifted_i, y_axis_low, y_axis_high, atl, ath))
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

if __name__ == "__main__":
    main()