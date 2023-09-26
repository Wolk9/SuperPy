# code to create the data files at first
import os
import csv
import datetime
from date_functions import get_today
from constants import DATA_DIR, TODAY_FILE, BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, INVENTORY_FILE, BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, INVENTORY_HEADER



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
    
    if not os.path.exists(EXPIRED_FILE):
        with open(EXPIRED_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(EXPIRED_HEADER)
            
    # Create today.txt if it doesn't exist
    if not os.path.exists(TODAY_FILE):
        with open(TODAY_FILE, "w") as f:
            today = datetime.date.today().strftime("%Y-%m-%d")
            f.write(today)



def update_inventory():
    # Read the bought products from the CSV file
    with open(TODAY_FILE, "r") as f:
        today = f.read().strip()
    with open(BOUGHT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        bought_products = list(reader)[1:]

    # Check each bought product for expiration
    inventory = []
    expired = []
    for product in bought_products:
        expiration_date = datetime.datetime.strptime(
            product[4], "%Y-%m-%d").date()
        if expiration_date < today:
            expired.append(product)
        else:
            inventory.append(product)

    # Write the inventory to the inventory CSV file
    with open(INVENTORY_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_name", "quantity",
                        "buy_date", "buy_price", "expiration_date"])
        for product in inventory:
            writer.writerow(
                [product[1], 1, product[2], product[3], product[4]])

    # Write the expired products to the expired CSV file
    with open(EXPIRED_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_name", "buy_date",
                        "buy_price", "expiration_date"])
        for product in expired:
            writer.writerow([product[1], product[2], product[3], product[4]])
