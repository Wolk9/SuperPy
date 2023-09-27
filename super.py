# Imports
import argparse
import csv
import datetime
import os
from tabulate import tabulate
from core.parser import create_parser
from functions.files import create_data_files
from functions.dates import get_today, set_today, advance_time
from functions.reports import get_inventory_report, get_revenue_report, get_profit_report, get_report_date
from functions.inventory import update_inventory
from functions.buy import buy_product
from functions.sell import sell_product

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

DATA_DIR = os.path.join(os.getcwd(), "data")
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
EXPIRED_FILE = os.path.join(DATA_DIR, "expired.csv")

def main():
    create_data_files()
    
    args = create_parser()
    
    parser = argparse.ArgumentParser()

    # Check which command was given
    # and call the corresponding function
    # with the given arguments

    # the set_today function is added to the parser
    if args.command == "set_today":
        set_today(datetime.datetime.strptime(args.date, "%Y-%m-%d").date())
        update_inventory()
    elif args.command == "get_today":
        print(get_today())
        update_inventory()
    # the advance_time function is added to the parser
    elif args.command == "advance_time":
        advance_time(args.days)
        update_inventory()
    # the buy function is added to the parser
    elif args.command == "buy":
        update_inventory()
        buy_product(args.product_name, args.price,
                    args.expiration_date, args.quantity)
    # the sell function is added to the parser
    elif args.command == "sell":
        update_inventory()
        sell_product(args.product_name, args.price, args.quantity)
    # the report function is added to the parser
    elif args.command == "report":
        update_inventory()
        report_date = get_report_date(args)

        # Check which report type was given

        # the inventory report is added to the parser
        if args.report_type == "inventory":
            if report_date:
                print(f"Inventory report for {report_date}:")
                get_inventory_report()

        # the revenue report is added to the parser
        elif args.report_type == "revenue":
            if report_date:
                revenue = get_revenue_report(report_date)
                print(f"Revenue for {report_date}: {revenue}")

        # the profit report is added to the parser
        elif args.report_type == "profit":
            if report_date:
                profit = get_profit_report(report_date)
                print(f"Profit for {report_date}: {profit}")

        else:
            parser.print_help()
            
            

    



def delete_bought_product(product_id):
    with open(BOUGHT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    with open(BOUGHT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(rows[0])
        for row in rows[1:]:
            if row[0] != product_id:
                writer.writerow(row)


if __name__ == "__main__":
    main()
