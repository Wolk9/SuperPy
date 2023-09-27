import csv
import datetime
from functions.dates import get_today
from core.constants import INVENTORY_FILE, SOLD_FILE, EXPIRED_FILE
from functions.inventory import get_next_id

# function to sell products that are on stock and not expired.
# In the inventory file there are separate records for the same product with another price.
# to sell a product it first should check how many products are in stock with the same name and are not expired.
# if there are enough products in stock, it sells the product and adds a record to the sold file.
# if there are not enough products in stock, it gives a message that there are not enough products in stock.


def sell_product(product_name, price, quantity=1):
    price = float(price)
    today = get_today()
    with open(INVENTORY_FILE, "r", newline="") as inventory_file, \
            open(SOLD_FILE, "a", newline="") as sold_file:
        inventory_reader = csv.reader(inventory_file)
        sold_writer = csv.writer(sold_file)

        # Find all products with the same name that are in stock
        products = []
        for row in inventory_reader:
            if row[1] == product_name and int(float(row[3])) > 0:
                row[3] = round(float(row[3]), 2)  # convert buy price to float
                row[4] = datetime.datetime.strptime(row[4], "%Y-%m-%d").date()  # convert expiration date to date object
                products.append(row)

        # Sort products by nearest expiring date and lowest buyprice
        products.sort(key=lambda x: (x[4], x[2]))

        # Check if there are enough products in stock
        total_quantity = sum(int(float(product[3])) for product in products)
        if total_quantity < quantity:
            print(f"Not enough {product_name}(s) in stock")
            if total_quantity > 0:
                answer = input(f"Do you want to sell the remaining {total_quantity} {product_name}(s)? (Yes/No) ")
                if answer.lower() == "yes":
                    quantity = total_quantity
                else:
                    return
            else:
                return

        # Sell the products and add a record to the sold file
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
                        price, sold_quantity]
            sold_writer.writerow(sold_row)
            product[3] = str(float(product[3]) - sold_quantity)

        # Update the inventory file
        with open(INVENTORY_FILE, "w", newline="") as inventory_file:
            inventory_writer = csv.writer(inventory_file)
            inventory_writer.writerows(products)

        print(f"Sold {sold_quantity} {product_name}(s)")