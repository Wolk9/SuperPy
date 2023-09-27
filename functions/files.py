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



