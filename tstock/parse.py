# Written by Gabe Banks 2022 <https://gabebanks.net>

import argparse
import os
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
    # Define these extremely long lists in one line because I don't feel like making a separate file for them
    crypto_symbols = ["1ST", "2GIVE", "808", "AAVE", "ABT", "ABY", "AC", "ACT", "ADA", "ADT", "ADX", "AE", "AEON", "AGI", "AGRS", "AI", "AID", "AION", "AIR", "AKY", "ALGO", "ALIS", "AMBER", "AMP", "AMPL", "ANC", "ANT", "APPC", "APX", "ARDR", "ARK", "ARN", "AST", "ATB", "ATM", "ATOM", "ATS", "AUR", "AVAX", "AVT", "B3", "BAND", "BAT", "BAY", "BBR", "BCAP", "BCC", "BCD", "BCH", "BCN", "BCPT", "BCX", "BCY", "BDL", "BEE", "BELA", "BET", "BFT", "BIS", "BITB", "BITBTC", "BITCNY", "BITEUR", "BITGOLD", "BITSILVER", "BITUSD", "BIX", "BLITZ", "BLK", "BLN", "BLOCK", "BLZ", "BMC", "BNB", "BNT", "BNTY", "BOST", "BOT", "BQ", "BRD", "BRK", "BRX", "BSV", "BTA", "BTC", "BTCB", "BTCD", "BTCP", "BTG", "BTM", "BTS", "BTSR", "BTT", "BTX", "BURST", "BUSD", "BUZZ", "BYC", "BYTOM", "C20", "CAKE", "CANN", "CAT", "CCRB", "CDT", "CFI", "CHAT", "CHIPS", "CLAM", "CLOAK", "CMP", "CMT", "CND", "CNX", "COFI", "COMP", "COSS", "COVAL", "CRBIT", "CREA", "CREDO", "CRO", "CRW", "CSNO", "CTR", "CTXC", "CURE", "CVC", "DAI", "DAR", "DASH", "DATA", "DAY", "DBC", "DBIX", "DCN", "DCR", "DCT", "DDF", "DENT", "DFS", "DGB", "DGC", "DGD", "DICE", "DLT", "DMD", "DMT", "DNT", "DOGE", "DOPE", "DOT", "DRGN", "DTA", "DTB", "DYN", "EAC", "EBST", "EBTC", "ECC", "ECN", "EDG", "EDO", "EFL", "EGC", "EGLD", "EKT", "ELA", "ELEC", "ELF", "ELIX", "EMB", "EMC", "EMC2", "ENG", "ENJ", "ENRG", "EOS", "EOT", "EQT", "ERC", "ETC", "ETH", "ETHD", "ETHOS", "ETN", "ETP", "ETT", "EVE", "EVX", "EXCL", "EXP", "FCT", "FIL", "FLDC", "FLO", "FLT", "FRST", "FTC", "FTT", "FUEL", "FUN", "GAM", "GAME", "GAS", "GBG", "GBX", "GBYTE", "GCR", "GEO", "GLD", "GNO", "GNT", "GOLOS", "GRC", "GRT", "GRS", "GRWI", "GTC", "GTO", "GUP", "GVT", "GXS", "HBAR", "HBN", "HEAT", "HMQ", "HPB", "HSR", "HT", "HUSH", "HVN", "HXX", "ICN", "ICX", "IFC", "IFT", "IGNIS", "INCNT", "IND", "INF", "INK", "INS", "INSTAR", "INT", "INXT", "IOC", "ION", "IOP", "IOST", "IOTA", "IOTX", "IQT", "ITC", "IXC", "IXT", "J8T", "JNT", "KCS", "KICK", "KIN", "KLAY", "KMD", "KNC", "KORE", "KSM", "LBC", "LCC", "LEND", "LEO", "LEV", "LGD", "LINDA", "LINK", "LKK", "LMC", "LOCI", "LOOM", "LRC", "LSK", "LTC", "LUN", "LUNA", "MAID", "MANA", "MATIC", "MAX", "MBRS", "MCAP", "MCO", "MDA", "MEC", "MED", "MEME", "MER", "MGC", "MGO", "MINEX", "MINT", "MIOTA", "MITH", "MKR", "MLN", "MNE", "MNX", "MOD", "MONA", "MRT", "MSP", "MTH", "MTN", "MUE", "MUSIC", "MYB", "MYST", "MZC", "NAMO", "NANO", "NAS", "NAV", "NBT", "NCASH", "NDC", "NEBL", "NEO", "NEOS", "NET", "NLC2", "NLG", "NMC", "NMR", "NOBL", "NOTE", "NPXS", "NSR", "NTO", "NULS", "NVC", "NXC", "NXS", "NXT", "OAX", "OBITS", "OCL", "OCN", "ODEM", "ODN", "OF", "OK", "OMG", "OMNI", "ONION", "ONT", "OPT", "ORN", "OST", "PART", "PASC", "PAY", "PBL", "PBT", "PFR", "PING", "PINK", "PIVX", "PIX", "PLBT", "PLR", "PLU", "POA", "POE", "POLY", "POSW", "POT", "POWR", "PPC", "PPT", "PPY", "PRG", "PRL", "PRO", "PST", "PTC", "PTOY", "PURA", "QASH", "QAU", "QLC", "QRK", "QRL", "QSP", "QTL", "QTUM", "QUICK", "QWARK", "R", "RADS", "RAIN", "RBIES", "RBX", "RBY", "RCN", "RDD", "RDN", "REC", "RED", "REP", "REQ", "RHOC", "RIC", "RISE", "RLC", "RLT", "RPX", "RRT", "RUFF", "RUNE", "RUP", "RVT", "SAFEX", "SALT", "SAN", "SBTC", "SC", "SEELE", "SEQ", "SHIB", "SHIFT", "SIB", "SIGMA", "SIGT", "SJCX", "SKIN", "SKY", "SLR", "SLS", "SMART", "SMT", "SNC", "SNGLS", "SNM", "SNRG", "SNT", "SOC", "SOL", "SOUL", "SPANK", "SPC", "SPHR", "SPR", "SNX", "SRN", "START", "STEEM", "STK", "STORJ", "STORM", "STQ", "STRAT", "STX", "SUB", "SWFTC", "SWIFT", "SWT", "SYNX", "SYS", "TAAS", "TAU", "TCC", "TFL", "THC", "THETA", "TIME", "TIX", "TKN", "TKR", "TKS", "TNB", "TNT", "TOA", "TRAC", "TRC", "TRCT", "TRIBE", "TRIG", "TRST", "TRUE", "TRUST", "TRX", "TUSD", "TX", "UBQ", "UKG", "ULA", "UNB", "UNI", "UNITY", "UNO", "UNY", "UP", "URO", "USDT", "UST", "UTK", "VEE", "VEN", "VERI", "VET", "VIA", "VIB", "VIBE", "VIVO", "VOISE", "VOX", "VPN", "VRC", "VRM", "VRS", "VSL", "VTC", "VTR", "WABI", "WAN", "WAVES", "WAX", "WBTC", "WCT", "WDC", "WGO", "WGR", "WINGS", "WPR", "WTC", "WTT", "XAS", "XAUR", "XBC", "XBY", "XCN", "XCP", "XDN", "XEL", "XEM", "NEM", "XHV", "XID", "XLM", "XMG", "XMR", "XMT", "XMY", "XPM", "XRL", "XRP", "XSPEC", "XST", "XTZ", "XUC", "XVC", "XVG", "XWC", "XZC", "XZR", "YEE", "YOYOW", "ZCC", "ZCL", "ZCO", "ZEC", "ZEN", "ZET", "ZIL", "ZLA", "ZRX"]
    valid_currencies = ["AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNH", "CNY", "COP", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "ICP", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RUR", "RWF", "SAR", "SBD", "SCR", "SDG", "SDR", "SEK", "SGD", "SHP", "SLL", "SOS", "SRD", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"]
    currency_symbols = {"AED": "د.إ", "AFN": "؋", "ALL": "L", "AMD": "֏", "ANG": "ƒ", "AOA": "Kz", "ARS": "$", "AUD": "$", "AWG": "ƒ", "AZN": "₼", "BAM": "KM", "BBD": "$", "BDT": "৳", "BGN": "лв", "BHD": ".د.ب", "BIF": "FBu", "BMD": "$", "BND": "$", "BOB": "$b", "BRL": "R$", "BSD": "$", "BTC": "฿", "BTN": "Nu.", "BWP": "P", "BYR": "Br", "BYN": "Br", "BZD": "BZ$", "CAD": "$", "CDF": "FC", "CHF": "CHF", "CLP": "$", "CNY": "¥", "COP": "$", "CRC": "₡", "CUC": "$", "CUP": "₱", "CVE": "$", "CZK": "Kč", "DJF": "Fdj", "DKK": "kr", "DOP": "RD$", "DZD": "دج", "EEK": "kr", "EGP": "£", "ERN": "Nfk", "ETB": "Br", "ETH": "Ξ", "EUR": "€", "FJD": "$", "FKP": "£", "GBP": "£", "GEL": "₾", "GGP": "£", "GHC": "₵", "GHS": "GH₵", "GIP": "£", "GMD": "D", "GNF": "FG", "GTQ": "Q", "GYD": "$", "HKD": "$", "HNL": "L", "HRK": "kn", "HTG": "G", "HUF": "Ft", "IDR": "Rp", "ILS": "₪", "IMP": "£", "INR": "₹", "IQD": "ع.د", "IRR": "﷼", "ISK": "kr", "JEP": "£", "JMD": "J$", "JOD": "JD", "JPY": "¥", "KES": "KSh", "KGS": "лв", "KHR": "៛", "KMF": "CF", "KPW": "₩", "KRW": "₩", "KWD": "KD", "KYD": "$", "KZT": "лв", "LAK": "₭", "LBP": "£", "LKR": "₨", "LRD": "$", "LSL": "M", "LTC": "Ł", "LTL": "Lt", "LVL": "Ls", "LYD": "LD", "MAD": "MAD", "MDL": "lei", "MGA": "Ar", "MKD": "ден", "MMK": "K", "MNT": "₮", "MOP": "MOP$", "MRO": "UM", "MRU": "UM", "MUR": "₨", "MVR": "Rf", "MWK": "MK", "MXN": "$", "MYR": "RM", "MZN": "MT", "NAD": "$", "NGN": "₦", "NIO": "C$", "NOK": "kr", "NPR": "₨", "NZD": "$", "OMR": "﷼", "PAB": "B/.", "PEN": "S/.", "PGK": "K", "PHP": "₱", "PKR": "₨", "PLN": "zł", "PYG": "Gs", "QAR": "﷼", "RMB": "￥", "RON": "lei", "RSD": "Дин.", "RUB": "₽", "RWF": "R₣", "SAR": "﷼", "SBD": "$", "SCR": "₨", "SDG": "ج.س.", "SEK": "kr", "SGD": "$", "SHP": "£", "SLL": "Le", "SOS": "S", "SRD": "$", "SSP": "£", "STD": "Db", "STN": "Db", "SVC": "$", "SYP": "£", "SZL": "E", "THB": "฿", "TJS": "SM", "TMT": "T", "TND": "د.ت", "TOP": "T$", "TRL": "₤", "TRY": "₺", "TTD": "TT$", "TVD": "$", "TWD": "NT$", "TZS": "TSh", "UAH": "₴", "UGX": "USh", "USD": "$", "UYU": "$U", "UZS": "лв", "VEF": "Bs", "VND": "₫", "VUV": "VT", "WST": "WS$", "XAF": "FCFA", "XBT": "Ƀ", "XCD": "$", "XOF": "CFA", "XPF": "₣", "YER": "﷼", "ZAR": "R", "ZWD": "Z$"}
    args = parser.parse_args()
    # Make a dictionary of the options for easier handling.
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

    try:
        # Autofit x and y size
        t = os.get_terminal_size()
        tx = t.columns
        ty = t.lines

        if opts["intervals_back"] == -1:
            opts["intervals_back"] = tx - opts['pad_x']*2 - 15
            if args.v:
                print("Automatically resizing x to fit...")
        if opts["max_y"] == -1:
            opts["max_y"] = ty - 6
            if args.v:
                print("Automatically resizing y to fit...")
    except:
        if args.v:
            print("Autosize failed, setting x and y to defaults...")
        if opts["intervals_back"] == -1:
            opts["intervals_back"] = 70
        if opts["max_y"] == -1:
            opts["max_y"] = 40
    

    # Infer the asset class from the input
    if '/' in opts['ticker']:
        if args.v:
            print("/ detected in input, forex asset class inferred.")
        opts['asset_class'] = "forex"
    elif opts['ticker'].upper() in crypto_symbols:
        if args.v:
            print("detected in crypto symbol, crypto asset class inferred.")
        opts['asset_class'] = "crypto"

    # Validate arguments for time interval and asset class
    if args.t:
        if args.t not in ['1min', '5min', '15min', '30min', '60min', 'day', 'week', 'month']:
            print(f"Invalid interval value {args.t}.")
            sys.exit(1)
    if opts['asset_class']:
        if not opts['asset_class'] in ['stock', 'crypto', 'forex']:
            print(f"Invalid class value {opts['asset_class']}.")
            sys.exit(1)
    
    # Handle currency symbol for -c option
    if args.c != 'USD' and opts['asset_class'] != 'crypto':
        print("Warning: the -c flag is only supported for asset type 'crypto'. It will be ignored.")
    if args.c != 'USD' and opts['asset_class'] == 'crypto':
        c = args.c.upper()
        if not c in valid_currencies:
            print(f"Invalid currency {c}")
            sys.exit(1)
        if c in list(currency_symbols.keys()):
            opts['currency_symbol'] = currency_symbols[c]
        else:
            opts['currency_symbol'] = ''
    
    # Handle currency symbol for forex
    if opts['asset_class'] == 'forex':
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

    arg.add_argument("-b", metavar="COUNT", type=int, default=-1,
        help="Number of time intervals back to go back. The number of candlesticks generated. Defaults to fill the terminal.")

    arg.add_argument("-w", action="store_true",
        help="Enables extra words of 'wisdom'.")

    arg.add_argument("-s", action="store_true",
        help="Short output, prints the last price only.")

    arg.add_argument("--chart", action="store_true",
        help="Print the chart only. Overrides -w.")

    arg.add_argument("-c", metavar="CURRENCY", type=str, default="USD",
        help="Set the currency. Only works with '-a crypto'. Defaults to 'USD'.")

    arg.add_argument("-y", metavar="LINES", type=int, default=-1,
        help="Height of the chart. Defaults to fill the terminal.")

    arg.add_argument("-a", metavar="CLASS", type=str, default='stock',
        help="The asset class of TICKER. Valid values are 'stock', 'crypto', and 'forex'. Autodetects depending on input ticker.")

    arg.add_argument("--padx", metavar="COLUMNS", type=int, default=5,
        help="Horizontal padding of the chart. Defaults to 5.")

    arg.add_argument("--pady", metavar="LINES", type=int, default=4,
        help="Vertical padding of the chart. Defaults to 4.")

    arg.add_argument("-v", action="store_true",
        help="Toggle verbosity.")

    arg.add_argument("--version", action="store_true",
        help="Print tstock version.")

    return arg
