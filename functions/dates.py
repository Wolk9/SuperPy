import os
from core.constants import TODAY_FILE
import datetime
# function to get the set fictive day to work with


def get_today():
   
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
        today_date = datetime.datetime.strptime(today_str, "%Y-%m-%d").date()
        print("Today's fictive date is:", today_date)
    return today_date

# funtion to set the date to work with


def set_today(date):
    with open(TODAY_FILE, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))
    print("Today's date set to:", date)

# function to advance the fictive date with the parser


def advance_time(days):
    print(f"Advancing time with {days} days...")
    today = get_today()
    new_date = today + datetime.timedelta(days=days)
    set_today(new_date)
