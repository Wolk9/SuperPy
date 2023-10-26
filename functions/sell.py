import csv
import datetime
from functions.dates import get_today
from functions.inventory import get_next_id
from core.constants import INVENTORY_FILE, SOLD_FILE, INVENTORY_HEADER, BOUGHT_FILE

# function to sell products that are on stock and not expired.
# In the INVENTORY_FILE there are separate records for each single product.
# In the INVENTORY_FILE each product has a unique bought_id, a product_name, a buy_date, a buy_price and an expiration_date.    
# to sell a product it first should check how many products are in stock with the same name and are not expired.
# if there are enough products in stock, it sells the product and adds a single record for each single sold product to the sold file.
# in addition the record with the correspondent bought_id should be removed from the bought file.
# the sold file contains records with a unique sold_id, a bought_id, a product_name, a sell_date and a sell_price.
# the BOUGHT_FILE contains records with a unique bought_id, a product_name, a buy_date, a buy_price and an expiration_date.
# if there are not enough products in stock, it gives a message that there are not enough products in stock and prompts the user if they would like to sell the rest of the stock available.

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


