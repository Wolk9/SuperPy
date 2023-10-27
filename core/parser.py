import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog="python super.py", description="Supermarket Inventory Management", epilog="Thanks for using SuperPy!")
    subparsers = parser.add_subparsers(
        dest="command", title="commands", help="No arguments displays an inventory table")

    # Get today command
    parser_get_today = subparsers.add_parser(
        "get_today", help="Get the current date")
    
    # Set today command
    parser_set_today = subparsers.add_parser(
        "set_today", help="Set the current date")
    parser_set_today.add_argument(
        "date", nargs='?', default=None, help="The date (YYYY-MM-DD) to set as today")
    parser_set_today.add_argument(
        "--today", nargs='?', const=True, default=False, help="Set the real today as today")
    parser_set_today.add_argument(
        "--now", nargs='?', const=True, default=False, help="Set the real today as today")

    parser_advance_time = subparsers.add_parser(
        "advance_time", help="Set the date forwards or backwards x days")
    parser_advance_time.add_argument(
        "days", type=int, help="The number of days to advance (can be negative))")

    parser_buy = subparsers.add_parser("buy", help="Buy a product or products")
    parser_buy.add_argument("-pn",
                            "--product-name", required=True, help="Name of the product (singular)")
    parser_buy.add_argument("-pr", "--price", type=float,
                            required=True, help="Price of the product")
    parser_buy.add_argument("-ed","--expiration-date", required=True,
                            help="Expiration date of the product (YYYY-MM-DD)")
    parser_buy.add_argument("-q","--quantity", type=int, default=1,
                            help="Quantity of the product to buy (default is 1)")

    parser_sell = subparsers.add_parser("sell", help="Sell a product or products")
    parser_sell.add_argument("-pn",
        "--product-name", required=True, help="Name of the product")
    parser_sell.add_argument("-pr",
        "--price", type=float, required=True, help="Selling price of the product")
    parser_sell.add_argument("-q", "--quantity", type=int, default=1, help="Quantity of the product to sell (default is 1)")

    # Report command with sub-parsers for different report types
    parser_report = subparsers.add_parser("report", help="Generate reports")
    subparsers_report = parser_report.add_subparsers(
        dest="report_type", title="report types")

    # Inventory report
    parser_report_inventory = subparsers_report.add_parser(
        "inventory", help="Generate inventory report")
    parser_report_inventory.add_argument(
        "--now", action="store_true", help="Generate report for today")
    parser_report_inventory.add_argument(
        "--yesterday", action="store_true", help="Generate report for yesterday")
    parser_report_inventory.add_argument(
        "--date", help="Generate report for a specific date (YYYY-MM-DD)")
    # Expired products report
    parser_report_expired = subparsers_report.add_parser(
        "expired", help="Generate now expired products report")

    # Revenue report
    parser_report_revenue = subparsers_report.add_parser(
        "revenue", help="Generate revenue report")
    parser_report_revenue.add_argument(
        "--today", action="store_true", help="Generate report for today")
    parser_report_revenue.add_argument(
        "--day", type=str, help="Generate report for a specific date (YYYY-MM-DD)")
    parser_report_revenue.add_argument(
        "--date", type=str, help="Generate report for a specific date (YYYY-MM-DD)")
    parser_report_revenue.add_argument(
        "--month", type=str, help="Generate report for a specific month (YYYY-MM)")
    parser_report_revenue.add_argument(
        "--year", type=str, help="Generate report for a specific year (YYYY)")
    parser_report_revenue.add_argument(
        "--all", action="store_true", help="Generate report for all time")
    
    # profit report
    parser_report_profit = subparsers_report.add_parser(
        "profit", help="Generate profit report")
    parser_report_profit.add_argument(
        "--today", action="store_true", help="Generate report for today")
    parser_report_profit.add_argument(
        "--day", type=str, help="Generate report for a specific date (YYYY-MM-DD)")
    parser_report_profit.add_argument(
        "--date", type=str, help="Generate report for a specific date (YYYY-MM-DD)")
    parser_report_profit.add_argument(
        "--month", type=str, help="Generate report for a specific month (YYYY-MM)")
    parser_report_profit.add_argument(
        "--year", type=str, help="Generate report for a specific year (YYYY)")
    parser_report_profit.add_argument(
        "--all", action="store_true", help="Generate report for all time")

    args = parser.parse_args()
    
    return args
