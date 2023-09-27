import csv
from functions.dates import get_today
from core.constants import BOUGHT_FILE
from functions.inventory import get_next_id


# function to buy products. I have added the quantity function.
# it checkes if the products with the same name and expiration date is already in the list.
# it also checks if the products with the same name have the same price.
# if so, it adds the quantity to the existing product.
# Otherwise it adds a new product record to the list.


def buy_product(product_name, price, expiration_date, quantity=1):
    price = float(price)
    today = get_today().strftime("%Y-%m-%d")

    for _ in range(quantity):
        bought_id = get_next_id(BOUGHT_FILE)
        row = [bought_id, product_name, today,
               round(float(price), 2), expiration_date]
        with open(BOUGHT_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    print(f"Bought {quantity} {product_name}(s)")
