import os
from DataFetcher.crawl import main as do_parse

CURRENT_PATH = os.getcwd()
def main():
    do_parse(
        input_path=os.path.join(CURRENT_PATH, 'stocknumber.csv'),
        output_path=os.path.join(CURRENT_PATH, 'Result/data'))


if __name__ == '__main__':
    main()
