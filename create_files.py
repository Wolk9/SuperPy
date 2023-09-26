# code to create the data files at first
import os
import csv
import datetime


DATA_DIR = os.path.join(os.getcwd(), "data")
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
EXPIRED_FILE = os.path.join(DATA_DIR, "expired.csv")

BOUGHT_HEADER = ["bought_id", "product_name",
                 "buy_date", "buy_price", "expiration_date"]
SOLD_HEADER = ["sold_id", "bought_id",
               "product-name", "sell_date", "sell_price"]
EXPIRED_HEADER = ["expired_id", "expiration_date",
                  "bought_id", "product_name", "buy_date", "buy_price"]


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
    
    if not os.path.exist(EXPIRED_FILE):
        with open(EXPIRED_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(EXPIRED_HEADER)
            
    # Create today.txt if it doesn't exist
    if not os.path.exists(TODAY_FILE):
        with open(TODAY_FILE, "w") as f:
            today = datetime.date.today().strftime("%Y-%m-%d")
            f.write(today)
