import os
from DataFetcher.crawl import main as do_parse
from DataFetcher.iwarrantCrawl import main as do_iwarrantCrawl
from DataFetcher.warning_stock import WarningStock

CURRENT_PATH = os.getcwd()
def main():
    input_path = os.path.join(CURRENT_PATH, 'stocknumber.csv')
    output_data_path = os.path.join(CURRENT_PATH, 'Result/data')
    output_warrant_path = os.path.join(CURRENT_PATH, 'Result/iwarrant_data')

    try:
        ws = WarningStock()
        warning_stock_data = ws.get_data()
        ws.update_csv(input_path)

        do_parse(
            input_path=input_path,
            output_path=output_data_path)
        do_iwarrantCrawl(
            input_path=input_path,
            output_path=output_warrant_path)
    except Exception as ex:
        print('exception: {}'.format(ex))
    


if __name__ == '__main__':
    main()
