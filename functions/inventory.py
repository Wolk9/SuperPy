import csv
import datetime
from core.constants import DATE_FORMAT, BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, INVENTORY_FILE, BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, INVENTORY_HEADER, COSTS_FILE, COSTS_HEADER
from functions.dates import get_today
from functions.richtable import output_table

def update_inventory():
    # Read the bought products from the CSV file
    print("Updating inventory...")
    today_date = get_today()
    with open(BOUGHT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        bought_products = list(reader)[1:]
    print(
        f"I'm comparing the bought products expiration date with the set date {today_date}.")
    # Check each bought product for expiration
    inventory = []
    expired = []
    for product in bought_products:
        product_id = product[0]
        product_name = product[1]
        buy_date = product[2]
        buy_price = round(float(product[3]), 2)  # convert buy price to float
        expiration_date = product[4]
        expiration_date_obj = datetime.datetime.strptime(
            expiration_date, DATE_FORMAT).date()
        if expiration_date_obj < today_date:
            expired.append([product_id, product_name, buy_date,
                           buy_price, expiration_date])
        else:
            inventory.append(
                [product_id, product_name, buy_date, buy_price, expiration_date])

    # Write the inventory to the inventory CSV file
    with open(INVENTORY_FILE, "w", newline="") as f:
        print(
            f"Found {len(inventory)} products that are not expired and wrote them to the inventory file.")
        writer = csv.writer(f)
        writer.writerow(INVENTORY_HEADER)
        for product in inventory:
            writer.writerow(product)

    # Write the expired products to the expired CSV file
    with open(EXPIRED_FILE, "w", newline="") as f:
        print(
            f"Found {len(expired)} products that are expired and wrote them to the expired products file.")
        writer = csv.writer(f)
        writer.writerow(EXPIRED_HEADER)
        for product in expired:
            writer.writerow(product)

    def update_inventory(trash=False):
        # Read the bought products from the CSV file
        print("Updating inventory...")
        today_date = get_today()
        with open(BOUGHT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            bought_products = list(reader)[1:]
        print(
            f"I'm comparing the bought products expiration date with the set date {today_date}.")

        # Check each bought product for expiration
        inventory = []
        expired = []
        for product in bought_products:
            product_id = product[0]
            product_name = product[1]
            buy_date = product[2]
            buy_price = round(float(product[3]), 2)  # convert buy price to float
            expiration_date = product[4]
            expiration_date_obj = datetime.datetime.strptime(
                expiration_date, DATE_FORMAT).date()
            if expiration_date_obj < today_date:
                expired.append([product_id, product_name, buy_date,
                               buy_price, expiration_date])
            else:
                inventory.append(
                    [product_id, product_name, buy_date, buy_price, expiration_date])

        # Write the inventory to the inventory CSV file
        with open(INVENTORY_FILE, "w", newline="") as f:
            print(
                f"Found {len(inventory)} products that are not expired and wrote them to the inventory file.")
            writer = csv.writer(f)
            writer.writerow(INVENTORY_HEADER)
            for product in inventory:
                writer.writerow(product)

        # Write the expired products to the expired CSV file
        with open(EXPIRED_FILE, "w", newline="") as f:
            print(
                f"Found {len(expired)} products that are expired and wrote them to the expired products file.")
            writer = csv.writer(f)
            writer.writerow(EXPIRED_HEADER)
            for product in expired:
                writer.writerow(product)

        

        # Ask the user if the expired products should be thrown away
        if trash and expired:
            answer = input(
                f"{len(expired)} products are expired. Should they be thrown away? (Yes/No) ")
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
                            total_price += float(row[4])
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
        elif trash and not expired:
            print("No expired products found.")


def get_next_id(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        rows = list(reader)  # Read all rows into a list
        if not rows:  # Check if the list is empty
            return 1  # Return 1 as the default ID if there are no rows
        next_id = max(int(row[0]) for row in rows) + 1
    return next_id


# TODO: the get_next_id function is used in the buy_product function. In the Sell product function the bought_id is used to identify the product it is thowing an error.

