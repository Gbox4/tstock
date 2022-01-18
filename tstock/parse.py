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
        "interval": "day",
        "intervals_back": 71,
        "equity": "stock",
        "max_y": 40,
        "pad_x": 5,
        "pad_y": 4,
        "verbose": False,
        "wisdom": False,
        "intraday": False,
        "chart_only": False,
    }

    # Parse arguments
    if args.t:
        if args.t not in ['1min', '5min', '15min', '30min', '60min', 'day', 'month', 'year']:
            print(f"Invalid interval value {args.t}.")
            sys.exit(1)
        opts["interval"] = args.t
        if 'min' in args.t:
            opts["intraday"] = True
    if args.b:
        opts["intervals_back"] = args.b
    if args.e:
        if not args.e in ['stock', 'crypto', 'forex']:
            print(f"Invalid equity value {args.e}.")
            sys.exit(1)
        opts["equity"] = args.e
    if args.y:
        opts["max_y"] = args.y
    if args.padx:
        opts["pad_x"] = args.padx
    if args.pady:
        opts["pad_y"] = args.pady
    if args.v:
        opts["verbose"] = args.v
    if args.chart:
        opts["chart_only"] = args.chart
    if args.w:
        opts["wisdom"] = args.w
    
    return opts



def get_args():
    """Get the script arguments."""
    description = "tstock - check stocks from the terminal"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("ticker", metavar="TICKER", nargs=1,
        help="Which ticker's data to pull.")

    arg.add_argument("-t", metavar="INTERVAL", type=str,
        help="Time interval of each candlestick. Valid values are '1min', '5min', '15min', '30min', '60min', 'day', 'week', or 'month'. Defaults to 'day'.")

    arg.add_argument("-b", metavar="COUNT", type=int,
        help="Number of time intervals back to go back. The number of candlesticks generated. Defaults to 71.")

    arg.add_argument("-e", metavar="EQUITY", type=str,
        help="The type of equity of TICKER. Valid values are 'stock', 'crypto', and 'forex'. Defaults to 'stock'.")

    arg.add_argument("-y", metavar="LINES", type=int,
        help="Height of the chart. Defaults to 40.")

    arg.add_argument("--padx", metavar="COLUMNS", type=int,
        help="Horizontal padding of the chart. Defaults to 5.")

    arg.add_argument("--pady", metavar="LINES", type=int,
        help="Vertical padding of the chart. Defaults to 4.")

    arg.add_argument("-v", action="store_true",
        help="Toggles verbosity.")

    arg.add_argument("--chart", action="store_true",
        help="Prints the chart only. Overrides -w.")

    arg.add_argument("-w", action="store_true",
        help="Prints some extra words of 'wisdom'.")

    arg.add_argument("--version", action="store_true",
        help="Print tstock version.")

    return arg