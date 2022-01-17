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


def get_args():
    """Get the script arguments."""
    description = "tstock - check stocks from the terminal"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("ticker", metavar="TICKER", nargs=1,
        help="Which ticker's data to pull.")

    arg.add_argument("-t", metavar="interval", type=str,
        help="Time interval of each candlestick. Valid values are 'day', 'week', or 'month'. Defaults to 'day'.")

    arg.add_argument("-b", metavar="count", type=int,
        help="Number of time intervals back to go back. The number of candlesticks generated. Defaults to 71.")

    arg.add_argument("-y", metavar="lines", type=int,
        help="Height of the chart. Defaults to 40.")

    arg.add_argument("--padx", metavar="columns", type=int,
        help="Horizontal padding of the chart. Defaults to 5.")

    arg.add_argument("--pady", metavar="lines", type=int,
        help="Vertical padding of the chart. Defaults to 4.")

    arg.add_argument("-v", action="store_true",
        help="Toggles verbosity.")

    arg.add_argument("-c", action="store_true",
        help="Prints the chart only. Overrides -w.")

    arg.add_argument("-w", action="store_true",
        help="Prints some extra words of 'wisdom'.")

    arg.add_argument("--version", action="store_true",
        help="Print tstock version.")

    return arg