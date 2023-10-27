import csv
from datetime import datetime
from functions.dates import get_today, set_today
from functions.inventory import update_inventory
from functions.richtable import output_table
from core.constants import REVENUE_FILE, INVENTORY_FILE, COSTS_FILE, BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, PROFIT_FILE
from core.constants import REVENUE_HEADER, INVENTORY_HEADER, COSTS_HEADER, BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, PROFIT_HEADER

# function to get the date from the parser to generate the report with.


def get_report_date(args):
    today = get_today()
    if args.report_type == "inventory":
        print("I see the arg is inventory")
        if args.now:
            return today
        elif args.yesterday:
            date = today - datetime.timedelta(days=1)
            return date
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    elif args.report_type == "revenue" or args.report_type == "profit":
        print("I see the arg is revenue or profit")
        if args.today:
            return today
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        elif args.month:
            return datetime.datetime.strptime(args.month, "%Y-%m").date()
        elif args.year:
            return datetime.datetime.strptime(args.year, "%Y").date()
        elif args.all:
            return "all"

    return None


def get_inventory_report(date):
    set_today(date)
    update_inventory()
    output_table("inventory")

    return None


def get_profit_report(date, report_type):
    # lodad data from CSV file
    print("I'm in the get_profit_report function with:", date, report_type)

    with open(SOLD_FILE, "r") as sold_file:
        next(sold_file)
        sold_data = [line.strip().split(",") for line in sold_file.readlines()]

    if report_type == "day":
        # filter all records of the day from the sold file

        filtered_data = []
        profit = 0
        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date == date:
                profit = profit + (float(record[5]) - float(record[4]))
        amount = f"€ {round(profit, 2):.2f}"
        profit_record = [date, amount]
        filtered_data.append(profit_record)

        print(filtered_data)

        write_profit_data(filtered_data, total=0)

    elif report_type == "month":
        # filter all records of the month from the sold file
        # calculate the total profit per day
        # put the total profit per day in a list
        # calculate the total profit of the month and put it in the key "Total"

        filtered_data = []
        days = []
        total = 0
        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date.month == date.month:
                if record_date not in days:
                    profit = 0
                    for record2 in sold_data:
                        record2_date = datetime.strptime(
                            record2[3], "%Y-%m-%d").date()
                        if record2_date.day == record_date.day and record2_date.month == record_date.month and record2_date.year == record_date.year:
                            profit = profit + \
                                (float(record2[5]) - float(record2[4]))
                amount = f"€ {round(profit, 2):.2f}"
                days.append(record_date)
        profit_record = [record_date, amount]
        filtered_data.append(profit_record)
        total += profit
        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_profit_data(filtered_data, total_valuta)

    elif report_type == "year":
        # filter all records of the year from the profit file
        # calculate the total profit per month
        # put the total profit per month in a list
        # calculate the total profit of the month and put it in the key "Total"

        filtered_data = []
        months = []
        total = 0

        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date.year == date.year:
                if record_date.month not in months:
                    profit = 0
                    for record2 in sold_data:
                        record2_date = datetime.strptime(
                            record2[3], "%Y-%m-%d").date()
                        if record2_date.month == record_date.month and record2_date.year == record_date.year:
                            profit = profit + \
                                (float(record2[5]) - float(record2[4]))
                    amount = f"€ {round(profit, 2):.2f}"
                    profit_record = [record_date.strftime("%Y-%m"), amount]
                    months.append(record_date.month)
                    filtered_data.append(profit_record)
                    total += profit
        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_profit_data(filtered_data, total_valuta)

    elif report_type == "all":
        # take all records profit file
        # calculate the total profit per year
        # put the total profit per year in a dictionary
        # calculate the total profit of the year and put it in the key "Total"

        filtered_data = []
        years = {}
        total = 0

        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            year = record_date.year
            if year not in years:
                years[year] = 0
            years[year] += float(record[5]) - float(record[4])

        for year, profit in years.items():
            amount = f"€ {round(profit, 2):.2f}"
            profit_record = [str(year), amount]
            filtered_data.append(profit_record)
            total += profit

        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_profit_data(filtered_data, total_valuta)

    set_today(date)
    update_inventory()

    output_table("profit")


def get_revenue_report(date, report_type):
    # lodad data from CSV file
    print("I'm in the get_revenue_report function with:", date, report_type)

    with open(SOLD_FILE, "r") as sold_file:
        next(sold_file)
        sold_data = [line.strip().split(",") for line in sold_file.readlines()]
    print(sold_data)

    if report_type == "day":
        # filter all records of the day from the sold file
        # calculate the total revenue per hour
        # put the total revenue per hour in a list
        # calculate the total revenue of the day and put it in the key "Total"

        filtered_data = []
        revenue = 0
        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date == date:
                revenue += float(record[5])
        amount = f"€ {round(revenue, 2):.2f}"
        revenue_record = [date, amount]
        filtered_data.append(revenue_record)

        print(filtered_data)

        write_revenue_data(filtered_data, total_valuta)

    elif report_type == "month":
        # filter all records of the given month from the sold file
        # calculate the total revenue per day
        # put the total revenue per day in a list
        # calculate the total revenue of the month and put it in the key "Total"

        filtered_data = []
        days = []
        total = 0
        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date.month == date.month:
                if record_date not in days:
                    revenue = 0
                    for record2 in sold_data:
                        record2_date = datetime.strptime(
                            record2[3], "%Y-%m-%d").date()
                        if record2_date.day == record_date.day and record2_date.month == record_date.month and record2_date.year == record_date.year:
                            revenue += float(record2[5])
                amount = f"€ {round(revenue, 2):.2f}"
                days.append(record_date)
        revenue_record = [record_date, amount]
        filtered_data.append(revenue_record)
        total += revenue
        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_revenue_data(filtered_data, total_valuta)

    elif report_type == "year":
        # filter all records of the year from the sold file
        # calculate the total revenue per month
        # put the total revenue per month in a list
        # calculate the total revenue of the year and put it in the key "Total"

        filtered_data = []
        months = []
        total = 0

        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            if record_date.year == date.year:
                if record_date.month not in months:
                    revenue = 0
                    for record2 in sold_data:
                        record2_date = datetime.strptime(
                            record2[3], "%Y-%m-%d").date()
                        if record2_date.month == record_date.month and record2_date.year == record_date.year:
                            revenue += float(record2[5])
                    amount = f"€ {round(revenue, 2):.2f}"
                    revenue_record = [record_date.strftime("%Y-%m"), amount]
                    months.append(record_date.month)
                    filtered_data.append(revenue_record)
                    total += revenue
        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_revenue_data(filtered_data, total_valuta)

    elif report_type == "all":
        # take all records revenue file
        # calculate the total revenue per year
        # put the total revenue per year in a dictionary
        # calculate the total revenue of the year and put it in the key "Total"

        filtered_data = []
        years = {}
        total = 0

        for record in sold_data:
            record_date = datetime.strptime(record[3], "%Y-%m-%d").date()
            year = record_date.year
            if year not in years:
                years[year] = 0
            years[year] += float(record[5])

        for year, revenue in years.items():
            amount = f"€ {round(revenue, 2):.2f}"
            revenue_record = [str(year), amount]
            filtered_data.append(revenue_record)
            total += revenue

        total_valuta = f"€ {round(total, 2):.2f}"
        print(filtered_data)
        write_revenue_data(filtered_data, total_valuta)

    set_today(date)
    update_inventory()

    output_table("revenue")


def write_profit_data(filtered_data, total=0):
    with open(PROFIT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(PROFIT_HEADER)
        for record in filtered_data:
            writer.writerow(record)
        if total != 0:
            writer.writerow(["Total", total])


def write_revenue_data(filtered_data, total=0):
    with open(REVENUE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(REVENUE_HEADER)
        for record in filtered_data:
            writer.writerow(record)
        if total != 0:
            writer.writerow(["Total", total])
