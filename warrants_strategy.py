import os
from DataFetcher.crawl import main as do_parse

""" This script for execute warrants strategy! """
CURRENT_PATH = os.getcwd()
def main():
    """ This script for execute warrants strategy! """
    do_parse(
        input_path=os.path.join(CURRENT_PATH, 'stocknumber.csv'),
        output_path=os.path.join(CURRENT_PATH, 'Result/data'))


if __name__ == '__main__':
    """ This script for execute warrants strategy! """
    main()
