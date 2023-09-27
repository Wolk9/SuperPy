import os
from core.constants import TODAY_FILE
import datetime
# function to get the set fictive day to work with


def get_today():
    print("Getting today's fictional date...")
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
    return datetime.datetime.strptime(today_str, "%Y-%m-%d").date()

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
