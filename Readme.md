# SuperPy: Supermarket Inventory Management Tool

SuperPy is a command-line based inventory management tool designed to keep track of supermarket products. It provides features to record buying and selling activities, produce various reports, and maintain the internal date system for managing transactions.

## Features

- **Date Management**: Set and advance the internal date to simulate daily operations.
- **Inventory Control**: Record the buying and selling of products.
- **Reporting**: Generate revenue, profit, and inventory reports.
- **Data Storage**: All transactions are stored in CSV format for easy reference.

## Installation

1. Ensure you have Python 3 installed.
2. Clone or download this repository to your local machine.
3. Navigate to the directory in the command line.
  
## Usage

1. **Set Current Date**:

   python super.py set_today YYYY-MM-DD

2. **Get Current Date**

   python super.py get_today

3. **Advance Current Date**

   python super.py advance_time <number_of_days>

   > _this can be a negative number to go back in time_

4. **Buy a Product**

   python super.py buy --product-name "Product Name" --price <buy_price> --expiration-date YYYY-MM-DD --quantity 5

   The --quantity option allows you to specify the quantity of the product to buy (default is 1).

5. **Sell a Product**

   python super.py sell --product-name "Product Name" --price <sell_price> --quantity 5

   The --quantity allows you to specify the quantity of the product to sell.

   > If the quantity is not sufficient, the program will ask if you would like to sell the rest


6. **Generate Reports**:
   - **Inventory Report**
     python super.py report inventory
     - --now           Generate report for today 
     - --yesterday     Generate report for yesterday
     - --date DAY      Generate report for specific date (YYYY-MM-DD)
   - **Expired Report**
     A report with all the expired products on the specified date
     - --now           Generate report for today 
     - --yesterday     Generate report for yesterday
     - --date DAY      Generate report for specific date (YYYY-MM-DD)
   - **Revenue Report**:
     python super.py report revenue
      - --today        Generate report for today
      - --day DAY      Generate report for a specific date (YYYY-MM-DD)
      - --date DATE    Generate report for a specific date (YYYY-MM-DD)
      - --month MONTH  Generate report for a specific month (YYYY-MM)
      - --year YEAR    Generate report for a specific year (YYYY)
      - --all          Generate report for all time
   - **Profit Report**:
     python super.py report profit
      - --today        Generate report for today
      - --day DAY      Generate report for a specific date (YYYY-MM-DD)
      - --date DATE    Generate report for a specific date (YYYY-MM-DD)
      - --month MONTH  Generate report for a specific month (YYYY-MM)
      - --year YEAR    Generate report for a specific year (YYYY)
      - --all          Generate report for all time

  
  
  The reports are created in CSV format with the respectivly name and displayed with _rich_ to the commandline.

## Data Storage

All transaction data is stored in CSV files located in the `data` directory:

- `bought.csv`: Contains details about products bought.
- `sold.csv`: Contains details about products sold.
- `inventory.csv`: Contains details about the not expired products.
- `expired.csv`: Contains details about expired products.

The program makes use of temporary CSV files to generate reports:
- `revenue.csv`: Contains the calculated revenue information
- `profit.csv`: Contains the calculated profit information

## Student Author
Martin de Bes

Date of submition for review: 27-10-2023
