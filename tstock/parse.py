import argparse
import sys
from .settings import __version__


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.version:
        parser.exit(0, f"tstock {__version__}\n")

def parse_args(parser):
    args = parser.parse_args()
    opts = {
        "ticker": args.ticker[0],
        "interval": args.t,
        "intervals_back": args.b,
        "equity": args.e,
        "max_y": args.y,
        "pad_x": args.padx,
        "pad_y": args.pady,
        "verbose": args.v,
        "wisdom": args.w,
        "intraday": 'min' in args.t,
        "chart_only": args.chart,
        "currency": args.c
    }

    # Validate arguments
    if args.t:
        if args.t not in ['1min', '5min', '15min', '30min', '60min', 'day', 'month', 'year']:
            print(f"Invalid interval value {args.t}.")
            sys.exit(1)
    if args.e:
        if not args.e in ['stock', 'crypto', 'forex']:
            print(f"Invalid equity value {args.e}.")
            sys.exit(1)
   
    # Print options if verbose
    if args.v:
        for k, v in opts.items():
            print(f"{k}: {v}")

    return opts



def get_args():
    """Get the script arguments."""
    description = "tstock - check stocks from the terminal"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("ticker", metavar="TICKER", nargs=1,
        help="Which ticker's data to pull.")

    arg.add_argument("-t", metavar="INTERVAL", type=str, default='day',
        help="Time interval of each candlestick. Valid values are '1min', '5min', '15min', '30min', '60min', 'day', 'week', or 'month'. Defaults to 'day'.")

    arg.add_argument("-b", metavar="COUNT", type=int, default=70,
        help="Number of time intervals back to go back. The number of candlesticks generated. Defaults to 70.")

    arg.add_argument("-e", metavar="EQUITY", type=str, default='stock',
        help="The type of equity of TICKER. Valid values are 'stock', 'crypto', and 'forex'. Defaults to 'stock'.")

    arg.add_argument("-w", action="store_false",
        help="Disables the extra words of 'wisdom'.")

    arg.add_argument("-y", metavar="LINES", type=int, default=40,
        help="Height of the chart. Defaults to 40.")

    arg.add_argument("--padx", metavar="COLUMNS", type=int, default=5,
        help="Horizontal padding of the chart. Defaults to 5.")

    arg.add_argument("--pady", metavar="LINES", type=int, default=4,
        help="Vertical padding of the chart. Defaults to 4.")

    arg.add_argument("-c", metavar="CURRENCY", type=str, default="USD",
        help="Set the currency. Only works with '-e crypto'. Defaults to 'USD'.")

    arg.add_argument("-v", action="store_true",
        help="Toggle verbosity.")

    arg.add_argument("--chart", action="store_true",
        help="Print the chart only. Overrides -w.")

    arg.add_argument("--version", action="store_true",
        help="Print tstock version.")

    return arg