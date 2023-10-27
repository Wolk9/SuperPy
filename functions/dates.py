# Import from python standard library
import os
import datetime
# Import from core folder
from core.constants import TODAY_FILE


# function to get the fictive date set to work with
def get_today(): 
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
        today_date = datetime.datetime.strptime(today_str, "%Y-%m-%d").date()
    return today_date

# funtion to set the date to work with
def set_today(date):
    with open(TODAY_FILE, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))
    get_today()

# function to advance the fictive date with the parser
def advance_time(days):
    today = get_today()
    new_date = today + datetime.timedelta(days=days)
    set_today(new_date)
