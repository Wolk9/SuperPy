from tabulate import tabulate
from core.constants import BOUGHT_HEADER, SOLD_HEADER, EXPIRED_HEADER, INVENTORY_FILE, COSTS_HEADER
from core.constants import BOUGHT_FILE, SOLD_FILE, EXPIRED_FILE, COSTS_FILE

def output_table(content_type):
    """
    Outputs a table to the CLI using the tabulate library.

    Args:
        content_type (str): The type of content to output.
        data_file (str): The filepath of the CSV data file to use for the table.

    Returns:
        None
    """
    # Determine headers based on content_type parameter
    if content_type == 'inventory':
        headers = BOUGHT_HEADER
        data_file = BOUGHT_FILE
    elif content_type == 'bought':
        headers = SOLD_HEADER
        data_file = SOLD_FILE
    elif content_type == 'sold':
        headers = EXPIRED_HEADER
        data_file = EXPIRED_FILE
    elif content_type == 'costs':
        headers = INVENTORY_FILE
        data_file = INVENTORY_FILE
    elif content_type == 'expired':
        headers = COSTS_HEADER
        data_file = COSTS_FILE
    else:
        raise ValueError('Invalid content type specified.')
    
    # Load data from CSV file
    with open(data_file, 'r') as f:
        next(f)  # skip the first line
        data = [line.strip().split(',') for line in f.readlines()]

    # Determine table format based on content_type parameter
    if content_type == 'inventory':
        table_format = 'fancy_grid'
    else:
        table_format = 'fancy_grid'

    # Output table to CLI
    print(tabulate(data, headers=headers, tablefmt=table_format))
