import os

# This file contains the constants used in the program

# Declare the data directory
DATA_DIR = os.path.join(os.getcwd(), "data")

# Declare the data files
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
EXPIRED_FILE = os.path.join(DATA_DIR, "expired.csv")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.csv")
COSTS_FILE = os.path.join(DATA_DIR, "costs.csv")
REVENUE_FILE = os.path.join(DATA_DIR, "revenue.csv")
PROFIT_FILE = os.path.join(DATA_DIR, "profit.csv")

# Declare the date format
DATE_FORMAT = "%Y-%m-%d"

# Declare the headers for the CSV files
BOUGHT_HEADER = ["bought_id", "product_name",
                 "buy_date", "buy_price", "expiration_date"]
SOLD_HEADER = ["sold_id",
               "product-name", "buy_date", "sell_date", "buy_price","sell_price"]
EXPIRED_HEADER = ["bought_id", "product_name",
                  "buy_date", "buy_price", "expiration_date"]
INVENTORY_HEADER = ["bought_id", "product_name",
                    "buy_date", "buy_price", "expiration_date"]
COSTS_HEADER = ["cost_id", "number_of_products", "cost_date", "total_cost"]  

REVENUE_HEADER = ["Period", "Revenue"]

PROFIT_HEADER = ["Period", "Profit"]
