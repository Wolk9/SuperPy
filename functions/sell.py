# Import from standard library
import csv
import datetime
# Import from functions folder
from functions.dates import get_today
# Import from core folder
from core.constants import INVENTORY_FILE, SOLD_FILE, INVENTORY_HEADER, BOUGHT_FILE

# This function is used to sell products.
# It checks if there are enough products in stock and if so, it updates the inventory and sold files.
# If there are not enough products in stock, it asks the user if he/she wants to sell the remaining products.
# If the user answers yes, the remaining products are sold.
# If the user answers no, the sale is cancelled.

def sell_product(product_name, price, quantity=1):
    
    # get today's date
    today = get_today()

    # read inventory file
    with open(INVENTORY_FILE, 'r') as f:
        reader = csv.DictReader(f)
        inventory = list(reader)

    # filter inventory by product name and expiration date
    filtered_inventory = [item for item in inventory if item['product_name'] == product_name and datetime.datetime.strptime(item['expiration_date'], '%Y-%m-%d').date() >= today]

    # check if there are enough products in stock
    if len(filtered_inventory) == 0: 
        print(f'No {product_name} foundin stock.')
    elif len(filtered_inventory) >= quantity:
        # sell products and update inventory and sold files
        sold_items = []
        with open(BOUGHT_FILE, 'r') as f:
            reader = csv.DictReader(f)
            bought_items = list(reader)
            for i in range(quantity):
                item = filtered_inventory[i]
                sold_item = {
                    'sold_id': item['bought_id'],
                    'product_name': item['product_name'],
                    'buy_date': item['buy_date'],
                    'sell_date': today,
                    'buy_price': item['buy_price'],
                    'sell_price': price
                }
                sold_items.append(sold_item)
                inventory.remove(item)
                bought_items = [bought_item for bought_item in bought_items if bought_item['bought_id'] != item['bought_id']]
        with open(INVENTORY_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=INVENTORY_HEADER)
            writer.writeheader()
            writer.writerows(inventory)
        with open(SOLD_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['sold_id', 'product_name', 'buy_date', 'sell_date','buy_price', 'sell_price'])
            writer.writerows(sold_items)
        with open(BOUGHT_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['bought_id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])
            writer.writeheader()
            writer.writerows(bought_items)
    else:
        answer = input(f"Not enough {product_name} in stock. Do you want to sell the remaining {len(filtered_inventory)} items? (y/n): ")
        if answer.lower() == 'y':
            quantity = len(filtered_inventory)
            sell_product(product_name, price, quantity)
        else:
            print("Sale cancelled.")


