import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog="SuperPy", description="Supermarket Inventory Management")
    subparsers = parser.add_subparsers(dest="command", title="commands")

    parser_set_today = subparsers.add_parser(
        "set_today", help="Set the current date")
    parser_set_today.add_argument(
        "date", help="The date (YYYY-MM-DD) to set as today")

    parser_advance_time = subparsers.add_parser(
        "advance_time", help="Advance the current date")
    parser_advance_time.add_argument(
        "days", type=int, help="The number of days to advance")

    parser_buy = subparsers.add_parser("buy", help="Buy a product")
    parser_buy.add_argument(
        "--product-name", required=True, help="Name of the product")
    parser_buy.add_argument("--price", type=float,
                            required=True, help="Price of the product")
    parser_buy.add_argument("--expiration-date", required=True,
                            help="Expiration date of the product (YYYY-MM-DD)")
    parser_buy.add_argument("--quantity", type=int, default=1,
                            help="Quantity of the product to buy (default is 1)")

    parser_sell = subparsers.add_parser("sell", help="Sell a product")
    parser_sell.add_argument(
        "--product-name", required=True, help="Name of the product")
    parser_sell.add_argument(
        "--price", type=float, required=True, help="Selling price of the product")

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

    # Revenue report
    parser_report_revenue = subparsers_report.add_parser(
        "revenue", help="Generate revenue report")
    group_revenue = parser_report_revenue.add_mutually_exclusive_group(
        required=True)
    group_revenue.add_argument(
        "--today", action="store_true", help="Generate report for today")
    group_revenue.add_argument(
        "--date", help="Generate report for a specific date (YYYY-MM-DD)")

    # Profit report
    parser_report_profit = subparsers_report.add_parser(
        "profit", help="Generate profit report")
    group_profit = parser_report_profit.add_mutually_exclusive_group(
        required=True)
    group_profit.add_argument(
        "--today", action="store_true", help="Generate report for today")
    group_profit.add_argument(
        "--date", help="Generate report for a specific date (YYYY-MM-DD)")

    args = parser.parse_args()

    return args
