import csv
import datetime
from functions.dates import get_today
from core.constants import INVENTORY_FILE, SOLD_FILE, INVENTORY_HEADER, EXPIRED_FILE
from functions.inventory import get_next_id

# function to sell products that are on stock and not expired.
# In the inventory file there are separate records for the same product with another price.
# to sell a product it first should check how many products are in stock with the same name and are not expired.
# if there are enough products in stock, it sells the product and adds a record to the sold file.
# if there are not enough products in stock, it gives a message that there are not enough products in stock.


def sell_product(product_name, price, quantity=1):
    # Round the price to two decimal places
    price = round(float(price), 2)

    # Get today's date
    today = get_today()

    # Read the inventory from the CSV file
    with open(INVENTORY_FILE, "r", newline="") as inventory_file:
        inventory_reader = csv.reader(inventory_file)
        inventory = list(inventory_reader)[1:]

    # Find all products with the same name that are in stock
    products = []
    available_quantity = 0
    for row in inventory:
        if row[1] == product_name and int(float(row[3])) > 0:
            print("Found product:", row)
            products.append(row)
            available_quantity += int(float(row[3]))


    # Check if there are enough products in stock
    if available_quantity < quantity:
        print(f"Not enough {product_name}(s) in stock")
        if available_quantity > 0:
            answer = input(
                f"Do you want to sell the remaining {available_quantity} {product_name}(s)? (Yes/No) ")
            if answer.lower() == "yes":
                quantity = available_quantity
            else:
                return
        else:
            return

    # Sell the products and update the inventory
    with open(INVENTORY_FILE, "w", newline="") as inventory_file, \
            open(SOLD_FILE, "a", newline="") as sold_file:
        inventory_writer = csv.writer(inventory_file)
        inventory_writer.writerow(INVENTORY_HEADER)
        sold_writer = csv.writer(sold_file)
        for product in products:
            if quantity == 0:
                break
            if int(float(product[3])) >= quantity:
                sold_quantity = quantity
            else:
                sold_quantity = int(float(product[3]))
            product_id = product[0]
            sold_id = get_next_id(SOLD_FILE)
            sold_row = [sold_id, product_id, product_name, today.strftime("%Y-%m-%d"),
                        round(float(price), 2), sold_quantity]
            sold_writer.writerow(sold_row)
            product[3] = str(round(float(product[3]), 2) - sold_quantity)
            if float(product[3]) > 0:
                inventory_writer.writerow(product)

            quantity -= sold_quantity

    print(f"Sold {sold_quantity} {product_name}(s)")