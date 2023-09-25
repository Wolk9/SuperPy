# Imports
import argparse
import csv
import datetime
import os
from tabulate import tabulate
from create_parser import create_parser

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

DATA_DIR = os.path.join(os.getcwd(), "data")
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
BOUGHT_HEADER = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]
SOLD_HEADER = ["id", "bought_id", "sell_date", "sell_price"]


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


# function to create the data files at first
def create_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create initial CSVs with headers if they don't exist
    if not os.path.exists(BOUGHT_FILE):
        with open(BOUGHT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(BOUGHT_HEADER)

    if not os.path.exists(SOLD_FILE):
        with open(SOLD_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(SOLD_HEADER)

# function to get the date today

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

# function to get the set fictive day to work with

def get_today():
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
    return datetime.datetime.strptime(today_str, "%Y-%m-%d").date()

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

# function to advance the fictive date with the parser

def advance_time(days):
    today = get_today()
    new_date = today + datetime.timedelta(days=days)
    set_today(new_date)

# function to buy products. I have added the quantity function.
# it checkes if the products with the same name and expiration date is already in the list.
# it also checks if the products with the same name have the same price.
# if so, it adds the quantity to the existing product. 
# Otherwise it adds a new product record to the list.
def buy_product(product_name, price, expiration_date, quantity=1):
    with open(BOUGHT_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if a product with the same name and expiration date already exists
    for row in rows:
        if row[1] == product_name and row[4] == expiration_date:
            if float(row[3]) == price:
                row[0] = get_next_id(BOUGHT_FILE)
                row[2] = get_today().strftime("%Y-%m-%d")
                row[3] = str(float(row[3]) + price)
                with open(BOUGHT_FILE, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                print(f"Bought {quantity} {product_name}(s) and added them to existing record")
                return

    # If the product doesn't exist, add a new record
    for _ in range(quantity):
        bought_id = get_next_id(BOUGHT_FILE)
        row = [bought_id, product_name, get_today().strftime("%Y-%m-%d"),
               price, expiration_date]
        with open(BOUGHT_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    print(f"Bought {quantity} {product_name}(s)")


# function to sell products that are on stock and not expired.
def sell_product(product_name, price, quantity=1):
    bought_ids = []
    with open(BOUGHT_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[1] == product_name and not is_product_sold(row[0]) and datetime.datetime.strptime(row[4], "%Y-%m-%d").date() >= get_today():
                bought_ids.append(row[0])

    if len(bought_ids) < quantity:
        print("There is not enough on stock.")
        return

    sold_ids = []
    for i in range(quantity):
        bought_id = bought_ids[i]
        sold_id = get_next_id(SOLD_FILE)
        row = [sold_id, bought_id, get_today().strftime("%Y-%m-%d"), price]
        with open(SOLD_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        sold_ids.append(sold_id)

    print(f"Sold {quantity} {product_name}(s) with IDs: {', '.join(str(id) for id in sold_ids)}")

# function to get the next ID of a product in the list
def get_next_id(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        rows = list(reader)  # Read all rows into a list
        if not rows:  # Check if the list is empty
            return 1  # Return 1 as the default ID if there are no rows
        next_id = max(int(row[0]) for row in rows) + 1
    return next_id

# function to get the product in stock if any.
def find_product_in_stock(product_name):
    if row[1] == product_name and not is_product_sold(row[0]):
        return row[0]
    return None

# function to see if a product is sold or not
def is_product_sold(bought_id, row):
    if row[1] == bought_id:
        return True
    return False


# function to get the inventory report.
def get_inventory_report():
    inventory_report = {}
    total_count = 0
    total_not_expired = 0
    total_expired = 0
    with open(BOUGHT_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if not is_product_sold(row[0], row):
                product_name = row[1]
                price = float(row[3])
                expiration_date = row[4]
                if product_name not in inventory_report:
                    inventory_report[product_name] = {}
                if price not in inventory_report[product_name]:
                    inventory_report[product_name][price] = {}
                if expiration_date not in inventory_report[product_name][price]:
                    inventory_report[product_name][price][expiration_date] = 0
                inventory_report[product_name][price][expiration_date] += 1
                total_count += 1
                if datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date() >= get_today():
                    total_not_expired += 1
                else:
                    total_expired += 1

    # Sort the inventory report by expiration date
    sorted_report = {}
    for product_name, prices in inventory_report.items():
        sorted_prices = {}
        for price, expirations in prices.items():
            sorted_expirations = {}
            for expiration_date, count in sorted(expirations.items()):
                sorted_expirations[expiration_date] = count
            sorted_prices[price] = sorted_expirations
        sorted_report[product_name] = sorted_prices

    # Display the inventory report in a table
    headers = ["Product Name", "Price", "Expiration Date", "Count"]
    table = []
    for product_name, prices in sorted_report.items():
        for price, expirations in prices.items():
            for expiration_date, count in expirations.items():
                table.append([product_name, price, expiration_date, count])
    print(tabulate(table, headers=headers))

    # Display the total number of products and expired products
    print(f"Total number of products: {total_count}")
    print(f"Total number of expired products per {get_today()}: {total_expired}")

    # Write the inventory report to a CSV file in the data folder
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    csv_file = os.path.join(data_folder, "inventory_report.csv")
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table)

# function to generate the revenue report
def get_revenue_report(report_date):
    revenue = 0
    with open(SOLD_FILE, "r") as sold_file:
        reader = csv.reader(sold_file)
        next(reader)  # Skip the header row
        for row in reader:
            sell_date_str = row[2]
            sell_date = datetime.datetime.strptime(
                sell_date_str, "%Y-%m-%d").date()
            if sell_date == report_date:
                revenue += float(row[3])
    
# function to generate the profit report
def get_profit_report(date):
    revenue = 0
    cost = 0
    with open(SOLD_FILE, "r") as sold_file:
        reader = csv.reader(sold_file)
        next(reader)  # Skip the header row
        for row in reader:
            sold_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
            if sold_date == date:
                sold_price = float(row[3])
                bought_id = row[1]
                # Calculate the cost for each sold item
                cost += get_buy_price(bought_id)
                revenue += sold_price
    return revenue - cost


# function to get the buy price in the bought list
def get_buy_price(bought_id):
    with open(BOUGHT_FILE, "r") as bought_file:
        reader = csv.reader(bought_file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == bought_id:
                return float(row[3])
    return 0.0

# function to get the quantity of a product in the bought list
def get_quantity_bought(bought_id):
    quantity = 0
    with open(BOUGHT_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == bought_id:
                quantity += 1
    return quantity


if __name__ == "__main__":
    main()

