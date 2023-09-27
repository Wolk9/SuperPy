import datetime
from functions.dates import get_today

# function to get the date from the parser to generate the report with.


def get_report_date(args):
    today = get_today()
    if args.report_type == "inventory":
        if args.now:
            return today
        elif args.yesterday:
            return today - datetime.timedelta(days=1)
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    elif args.report_type == "revenue" or args.report_type == "profit":
        if args.today:
            return today
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    return None


def get_inventory_report():
    return None


def get_revenue_report():
    return None


def get_profit_report():
    return None 
