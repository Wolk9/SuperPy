import os

DATA_DIR = os.path.join(os.getcwd(), "data")
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
EXPIRED_FILE = os.path.join(DATA_DIR, "expired.csv")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.csv")

BOUGHT_HEADER = ["bought_id", "product_name",
                 "buy_date", "buy_price", "expiration_date"]
SOLD_HEADER = ["sold_id", "bought_id",
               "product-name", "sell_date", "sell_price"]
EXPIRED_HEADER = ["expired_id", "expiration_date",
                  "bought_id", "product_name", "buy_date", "buy_price"]
INVENTORY_HEADER = ["bought_id", "product_name",
                    "quantity", "buy_date", "buy_price", "expiration_date"]
