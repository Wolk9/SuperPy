# Imports
import argparse
import csv
import datetime
import os
from tabulate import tabulate
from create_files import create_data_files
from create_parser import create_parser

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.



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
    elif args.command == "get_today":
        print(get_today())
    # the advance_time function is added to the parser
    elif args.command == "advance_time":
        advance_time(args.days)
    # the buy function is added to the parser
    elif args.command == "buy":
        buy_product(args.product_name, args.price,
                    args.expiration_date, args.quantity)
    # the sell function is added to the parser
    elif args.command == "sell":
        sell_product(args.product_name, args.price, args.quantity)
    # the report function is added to the parser
    elif args.command == "report":
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
            
        
            

def get_today():
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
    return datetime.datetime.strptime(today_str, "%Y-%m-%d").date()

# funtion to set the date to work with


def set_today(date):
    with open(TODAY_FILE, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))
    print("Today's date set to:", date)



if __name__ == "__main__":
    main()
