# code to create the data files at first
import os
import csv
import datetime
from functions.dates import get_today
from core.constants import DATE_FORMAT, DATA_DIR, TODAY_FILE, BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, INVENTORY_FILE, BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, INVENTORY_HEADER, COSTS_FILE, COSTS_HEADER   



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
    
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(INVENTORY_HEADER)
    
    if not os.path.exists(COSTS_FILE):
        with open(COSTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(COSTS_HEADER)

    # Create today.txt if it doesn't exist
    if not os.path.exists(TODAY_FILE):
        with open(TODAY_FILE, "w") as f:
            today = datetime.date.today().strftime("%Y-%m-%d")
            f.write(today)


def update_inventory():
    # Read the bought products from the CSV file
    print("Updating inventory...")
    today_date = get_today()
    with open(BOUGHT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        bought_products = list(reader)[1:]
    print(f"I'm comparing the bought products expiration date with the set date {today_date}.")
    # Check each bought product for expiration
    inventory = []
    expired = []
    for product in bought_products:
        product_id = product[0]
        product_name = product[1]
        buy_date = product[2]
        buy_price = product[3]
        expiration_date = product[4]
        expiration_date_obj = datetime.datetime.strptime(
            expiration_date, DATE_FORMAT).date()
        if expiration_date_obj < today_date:
            expired.append([product_id, product_name, buy_date, buy_price, expiration_date])
        else:
            inventory.append([product_id, product_name, buy_date, buy_price, expiration_date])

    # Write the inventory to the inventory CSV file
    with open(INVENTORY_FILE, "w", newline="") as f:
        print(f"Found {len(inventory)} products that are not expired and wrote them to the inventory file.")
        writer = csv.writer(f)
        writer.writerow(INVENTORY_HEADER)
        for product in inventory:
            writer.writerow(product)

    # Write the expired products to the expired CSV file
    with open(EXPIRED_FILE, "w", newline="") as f:
        print(f"Found {len(expired)} products that are expired and wrote them to the expired products file.")
        writer = csv.writer(f)
        writer.writerow(EXPIRED_HEADER)
        for product in expired:
            writer.writerow(product)

    # Ask the user if the expired products should be thrown away
    if expired:
        answer = input(f"{len(expired)} products are expired. Should they be thrown away? (Yes/No) ")
        if answer.lower() == "yes":
            # Delete the expired products from the bought CSV file
            with open(BOUGHT_FILE, "r", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)

            with open(BOUGHT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(rows[0])
                total_price = 0
                for row in rows[1:]:
                    if row[0] not in [product[0] for product in expired]:
                        writer.writerow(row)
                    else:
                        total_price += float(row[3])
            print(f"Deleted {len(expired)} products from the bought file.")

            # Write the trashed products to the costs CSV file
            with open(COSTS_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([len(expired), get_today(), total_price])
            print(f"Wrote trashed products to the costs file.")
            
            # Delete the expired products from the expired CSV file
            with open(EXPIRED_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(EXPIRED_HEADER)
            print(f"Deleted {len(expired)} products from the expired file.")
        else:
            print("Expired products were not thrown away.")
    else:
        print("No expired products found.")
