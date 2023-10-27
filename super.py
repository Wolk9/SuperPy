# Imports
import argparse
import csv
import datetime
import os
from rich import print
from tabulate import tabulate
from core.parser import create_parser
from functions.files import create_data_files
from functions.dates import get_today, set_today, advance_time
from functions.reports import get_inventory_report, get_revenue_report, get_profit_report
from functions.inventory import update_inventory
from functions.buy import buy_product
from functions.sell import sell_product
from functions.richtable import output_table

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
    
    # parser = argparse.ArgumentParser()

    # Check which command was given
    # and call the corresponding function
    # with the given arguments

    # the set_today function is added to the parser
    if args.command == "set_today":
        if args.date:
            set_today(datetime.datetime.strptime(args.date, "%Y-%m-%d").date())
            date = get_today()
        if args.now or args.today:
           set_today(datetime.date.today())
           date = get_today()
        print(f'Today\'s fictive date is now set to {date}.')
        update_inventory()
       
    elif args.command == "get_today":
        date = get_today()
        print(f'Today\'s fictive date is {date}.')
        update_inventory()
       
    # the advance_time function is added to the parser
    elif args.command == "advance_time":
        print(f"Advancing time with {args.days} days...")
        advance_time(args.days)
        date = get_today()
        print(f'Today\'s fictive date is now set to {date}.')
        update_inventory()
       
    # the buy function is added to the parser
    elif args.command == "buy":
        update_inventory()
        buy_product(args.product_name, args.price,
                    args.expiration_date, args.quantity)
        output_table("bought")
    # the sell function is added to the parser
    elif args.command == "sell":
        update_inventory()
        sell_product(args.product_name, args.price, args.quantity)
        output_table("sold")
    # the report function is added to the parser
    elif args.command == "report":
        
        # Check which report type was given

        # the inventory report is added to the parser
        if args.report_type == "inventory":
            today = get_today()
            if args.now:
                print(f"Inventory report for {today}:")
                get_inventory_report(today)
            if args.yesterday:
                yesterday = today - datetime.timedelta(days=1)
                print(f"Inventory report for {yesterday}:")
                get_inventory_report(yesterday)
            if args.date:
                report_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
                print(f"Inventory report for {report_date}:")
                current_date = get_today()
                set_today(report_date)
                get_inventory_report(report_date)
                set_today(current_date)
            
        # the expired report is added to the parser
        if args.report_type == "expired":
            today = get_today()
            print(f"Expired products report for {today}:")
            output_table("expired")

        # the revenue report is added to the parser
        elif args.report_type == "revenue":
            today = get_today()
            print(f"Revenue report per {today}:")
            if args.today:
                get_revenue_report(today, "day")
            if args.date or args.day:
                if args.date:
                    report_date = datetime.datetime.strptime(
                        args.date, "%Y-%m-%d").date()
                elif args.day:
                    report_date = datetime.datetime.strptime(
                        args.day, "%Y-%m-%d").date()
                print(f"for {report_date}:")
                current_date = get_today()
                set_today(report_date)
                get_revenue_report(report_date, "day")
                set_today(current_date)
            if args.month:
                report_date = datetime.datetime.strptime(args.month, "%Y-%m").date()
                print(f"for month {report_date.month} of {report_date.year}:")
                current_date = get_today()
                set_today(report_date)
                get_revenue_report(report_date, "month")
                set_today(current_date)
            if args.year:
                report_date = datetime.datetime.strptime(args.year, "%Y").date()
                print(f"for {report_date.year}:")
                current_date = get_today()
                set_today(report_date)
                get_revenue_report(report_date, "year")
                set_today(current_date)
            if args.all:
                print(f"for all time:")
                get_revenue_report(today, "all")

        # the profit report is added to the parser
        elif args.report_type == "profit":
            today = get_today()
            print(f"Profit report for {today}:")
            if args.today:
                get_profit_report(today, "day")
            if args.date or args.day:
                if args.date:
                    report_date = datetime.datetime.strptime(
                        args.date, "%Y-%m-%d").date()
                elif args.day:
                    report_date = datetime.datetime.strptime(args.day, "%Y-%m-%d").date()
                print(f"for {report_date}:")
                current_date = get_today()
                set_today(report_date)
                get_profit_report(report_date, "day")
                set_today(current_date)
            if args.month:
                report_date = datetime.datetime.strptime(args.month, "%Y-%m").date()
                print(f"for month {report_date.month} of {report_date.year}:")
                current_date = get_today()
                set_today(report_date)
                get_profit_report(report_date, "month")
                set_today(current_date)
            if args.year:
                report_date = datetime.datetime.strptime(args.year, "%Y").date()
                print(f"for {report_date.year}:")
                current_date = get_today()
                set_today(report_date)
                get_profit_report(report_date, "year")
                set_today(current_date)
            if args.all:
                print(f"for all time:")
                get_profit_report(today, "all")

        else:
            args.parser.print_help()
    else: 
        date = get_today()
        print("We pretent today's date is", date)
        update_inventory()
        output_table("inventory")        
            

    



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
