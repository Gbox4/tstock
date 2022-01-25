# Written by Gabe Banks 2022 <https://gabebanks.net>

import argparse
from locale import currency
import sys
from .settings import __version__, extra_help


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()
    if args.version:
        print(f"tstock {__version__}\nWritten by Gabe Banks 2022 <https://gabebanks.net>")
        sys.exit(0)

    if not args.ticker:
        parser.print_help()
        sys.exit(1)


def parse_args(parser):
    """Parse args."""
    currency_symbols = {"AED": "د.إ", "AFN": "؋", "ALL": "L", "AMD": "֏", "ANG": "ƒ", "AOA": "Kz", "ARS": "$", "AUD": "$", "AWG": "ƒ", "AZN": "₼", "BAM": "KM", "BBD": "$", "BDT": "৳", "BGN": "лв", "BHD": ".د.ب", "BIF": "FBu", "BMD": "$", "BND": "$", "BOB": "$b", "BRL": "R$", "BSD": "$", "BTC": "฿", "BTN": "Nu.", "BWP": "P", "BYR": "Br", "BYN": "Br", "BZD": "BZ$", "CAD": "$", "CDF": "FC", "CHF": "CHF", "CLP": "$", "CNY": "¥", "COP": "$", "CRC": "₡", "CUC": "$", "CUP": "₱", "CVE": "$", "CZK": "Kč", "DJF": "Fdj", "DKK": "kr", "DOP": "RD$", "DZD": "دج", "EEK": "kr", "EGP": "£", "ERN": "Nfk", "ETB": "Br", "ETH": "Ξ", "EUR": "€", "FJD": "$", "FKP": "£", "GBP": "£", "GEL": "₾", "GGP": "£", "GHC": "₵", "GHS": "GH₵", "GIP": "£", "GMD": "D", "GNF": "FG", "GTQ": "Q", "GYD": "$", "HKD": "$", "HNL": "L", "HRK": "kn", "HTG": "G", "HUF": "Ft", "IDR": "Rp", "ILS": "₪", "IMP": "£", "INR": "₹", "IQD": "ع.د", "IRR": "﷼", "ISK": "kr", "JEP": "£", "JMD": "J$", "JOD": "JD", "JPY": "¥", "KES": "KSh", "KGS": "лв", "KHR": "៛", "KMF": "CF", "KPW": "₩", "KRW": "₩", "KWD": "KD", "KYD": "$", "KZT": "лв", "LAK": "₭", "LBP": "£", "LKR": "₨", "LRD": "$", "LSL": "M", "LTC": "Ł", "LTL": "Lt", "LVL": "Ls", "LYD": "LD", "MAD": "MAD", "MDL": "lei", "MGA": "Ar", "MKD": "ден", "MMK": "K", "MNT": "₮", "MOP": "MOP$", "MRO": "UM", "MRU": "UM", "MUR": "₨", "MVR": "Rf", "MWK": "MK", "MXN": "$", "MYR": "RM", "MZN": "MT", "NAD": "$", "NGN": "₦", "NIO": "C$", "NOK": "kr", "NPR": "₨", "NZD": "$", "OMR": "﷼", "PAB": "B/.", "PEN": "S/.", "PGK": "K", "PHP": "₱", "PKR": "₨", "PLN": "zł", "PYG": "Gs", "QAR": "﷼", "RMB": "￥", "RON": "lei", "RSD": "Дин.", "RUB": "₽", "RWF": "R₣", "SAR": "﷼", "SBD": "$", "SCR": "₨", "SDG": "ج.س.", "SEK": "kr", "SGD": "$", "SHP": "£", "SLL": "Le", "SOS": "S", "SRD": "$", "SSP": "£", "STD": "Db", "STN": "Db", "SVC": "$", "SYP": "£", "SZL": "E", "THB": "฿", "TJS": "SM", "TMT": "T", "TND": "د.ت", "TOP": "T$", "TRL": "₤", "TRY": "₺", "TTD": "TT$", "TVD": "$", "TWD": "NT$", "TZS": "TSh", "UAH": "₴", "UGX": "USh", "USD": "$", "UYU": "$U", "UZS": "лв", "VEF": "Bs", "VND": "₫", "VUV": "VT", "WST": "WS$", "XAF": "FCFA", "XBT": "Ƀ", "XCD": "$", "XOF": "CFA", "XPF": "₣", "YER": "﷼", "ZAR": "R", "ZWD": "Z$"}
    valid_currencies = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNH", "CNY", "COP", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "ICP", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RUR", "RWF", "SAR", "SBD", "SCR", "SDG", "SDR", "SEK", "SGD", "SHP", "SLL", "SOS", "SRD", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"]
    args = parser.parse_args()
    opts = {
        "ticker": args.ticker,
        "interval": args.t,
        "intervals_back": args.b,
        "asset_class": args.a,
        "max_y": args.y,
        "pad_x": args.padx,
        "pad_y": args.pady,
        "verbose": args.v,
        "wisdom": args.w,
        "intraday": 'min' in args.t,
        "chart_only": args.chart,
        "currency": args.c,
        "short": args.s,
        "currency_symbol": "$",
    }

    # Validate arguments
    if args.t:
        if args.t not in ['1min', '5min', '15min', '30min', '60min', 'day', 'week', 'month']:
            print(f"Invalid interval value {args.t}.")
            sys.exit(1)
    if args.a:
        if not args.a in ['stock', 'crypto', 'forex']:
            print(f"Invalid class value {args.a}.")
            sys.exit(1)
    
    # Handle currency symbol for -c option
    if args.c != 'USD' and args.a != 'crypto':
        print("Warning: the -c flag is only supported for asset type 'crypto'. It will be ignored.")
    if args.c != 'USD' and args.a == 'crypto':
        c = args.c.upper()
        if not c in valid_currencies:
            print(f"Invalid currency {c}")
            sys.exit(1)
        if c in list(currency_symbols.keys()):
            opts['currency_symbol'] = currency_symbols[args.c]
        else:
            opts['currency_symbol'] = ''
    
    # Handle currency symbol for forex
    if args.a == 'forex':
        if args.ticker.count("/") != 1:
            print("Please delimit currency pairs with a slash, like FROM_CURRENCY/TO_CURRENCY. Ex: tstock -a forex USD/CNY")
            sys.exit(1)
        ticker = args.ticker.split("/")
        from_currency = ticker[0].upper()
        to_currency = ticker[1].upper()
        if not from_currency in valid_currencies:
            print(f"Invalid currency {from_currency}")
            sys.exit(1)
        if not to_currency in valid_currencies:
            print(f"Invalid currency {to_currency}")
            sys.exit(1)
        if to_currency in list(currency_symbols.keys()):
            opts['currency_symbol'] = currency_symbols[to_currency]
        else:
            opts['currency_symbol'] = ''

    # Print options if verbose
    if args.v:
        for k, v in opts.items():
            print(f"{k}: {v}")

    return opts



def get_args():
    """Get the script arguments."""
    description = "tstock - generate stock charts in the terminal."
    arg = argparse.ArgumentParser(description=description, epilog=extra_help, formatter_class=argparse.RawTextHelpFormatter)

    arg.add_argument("ticker", metavar="TICKER", nargs='?',
        help="Which ticker's data to pull.")

    arg.add_argument("-t", metavar="INTERVAL", type=str, default='day',
        help="Time interval of each candlestick. Valid values are '1min', '5min', '15min', '30min', '60min', 'day', 'week', or 'month'. Defaults to 'day'.")

    arg.add_argument("-b", metavar="COUNT", type=int, default=70,
        help="Number of time intervals back to go back. The number of candlesticks generated. Defaults to 70.")

    arg.add_argument("-a", metavar="CLASS", type=str, default='stock',
        help="The asset class of TICKER. Valid values are 'stock', 'crypto', and 'forex'. Defaults to 'stock'.")

    arg.add_argument("-s", action="store_true",
        help="Short output, prints the last price only.")

    arg.add_argument("--chart", action="store_true",
        help="Print the chart only. Overrides -w.")

    arg.add_argument("-c", metavar="CURRENCY", type=str, default="USD",
        help="Set the currency. Only works with '-a crypto'. Defaults to 'USD'.")

    arg.add_argument("-w", action="store_true",
        help="Enables extra words of 'wisdom'.")

    arg.add_argument("-y", metavar="LINES", type=int, default=40,
        help="Height of the chart. Defaults to 40.")

    arg.add_argument("--padx", metavar="COLUMNS", type=int, default=5,
        help="Horizontal padding of the chart. Defaults to 5.")

    arg.add_argument("--pady", metavar="LINES", type=int, default=4,
        help="Vertical padding of the chart. Defaults to 4.")

    arg.add_argument("-v", action="store_true",
        help="Toggle verbosity.")

    arg.add_argument("--version", action="store_true",
        help="Print tstock version.")

    return arg