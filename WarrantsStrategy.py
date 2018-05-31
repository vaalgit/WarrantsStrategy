from DataFetcher.crawl import main as do_parse
import os

current_path = os.getcwd()



def main():
    do_parse(
        input_path=os.path.join(current_path,'stocknumber.csv'),
        output_path=os.path.join(current_path,'Result/data'))

if __name__ == '__main__':
    main()