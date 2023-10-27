from rich.table import Table
from rich.console import Console
from core.constants import BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, INVENTORY_HEADER, COSTS_HEADER, REVENUE_HEADER, PROFIT_HEADER
from core.constants import BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, COSTS_FILE, INVENTORY_FILE, REVENUE_FILE, PROFIT_FILE
from functions.dates import get_today

def output_table(content_type, selection=None):

    """
    Outputs a table to the CLI using the rich.table library.

    Args:
        content_type (str): The type of content to output.

    Returns:
        None
    """
    # Determine headers and data_file based on content_type parameter
    if content_type == 'inventory':
        headers = INVENTORY_HEADER
        data_file = INVENTORY_FILE    
    elif content_type == 'bought':
        headers = BOUGHT_HEADER
        data_file = BOUGHT_FILE
    elif content_type == 'sold':
        headers = SOLD_HEADER
        data_file = SOLD_FILE
    elif content_type == 'costs':
        headers = COSTS_HEADER
        data_file = COSTS_FILE
    elif content_type == 'expired':
        headers = EXPIRED_HEADER
        data_file = EXPIRED_FILE
    elif content_type == 'revenue':
        headers = REVENUE_HEADER
        data_file = REVENUE_FILE            
    elif content_type == 'profit':
        headers = PROFIT_HEADER
        data_file = PROFIT_FILE
    else:
        raise ValueError('Invalid content type specified.')
    
    
    # Load data from CSV file
    with open(data_file, 'r') as f:
        next(f)  # skip the first line
        data = [line.strip().split(',') for line in f.readlines()]
        footer = None
        if len(data) > 1:
            if data[-1][0] == 'Total':
                footer = data[-1]
                data = data[:-1]

    # Create table object
    if selection is not None:
        title = f"\n {selection.capitalize()} {content_type.capitalize()} table:"
    else:
        title = f"\n {content_type.capitalize()} table:"
    table = Table(title=title, show_header=True,
                      header_style="bold magenta")

    for header in headers:
        if 'price' in header.lower():
            table.add_column(header, justify="right")
        else:
            table.add_column(header)


    # Define a list of valid styles
    colors = ["red", "blue", "green", "yellow", "magenta", "cyan", "white", "bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]
    # Create a dictionary to map each product type to a valid style
    color_dict = {}
    for i, row in enumerate(data):
        product_type = row[1]
        if product_type not in color_dict:
            color_dict[product_type] = colors[i % len(colors)]
        table.add_row(*row, style=color_dict[product_type])
    if footer:
        table.add_row("")
        table.add_row(*footer, style="bold magenta ")
    # Output table to CLI
    console = Console()
    console.print(table)
