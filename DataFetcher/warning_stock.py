import time
import json
import requests
import csv

from DataFetcher.utils.errors import CrawlRuntimeError
from datetime import datetime
from DataFetcher.utils.recorder import Recorder

class SORTKIND:
    STKNO='STKNO'

class QUERYTYPE:
    TYPE_1='1'

class WarningStockRecorder(Recorder):
    def __init__(self, path='../Result/data'):
        Recorder.__init__(self,path)
        
    def record_to_csv(self, data):
        """
        must override
        """
        pass

class WarningStock:
    def __init__(self, *args, **kwargs):
        """
        Get warning stock from twse
        """
        endpoint = 'http://www.twse.com.tw/announcement/notice'
        # Add 1000 seconds for prevent time inaccuracy
        timestamp = int(time.time() * 1000 + 1000000)
        startDate = datetime.now().date().strftime("%Y%m%d")
        endDate = datetime.now().date().strftime("%Y%m%d")
        sortKind = SORTKIND.STKNO
        querytype = QUERYTYPE.TYPE_1
        self.query_url = '{}?response=josn&startDate={}&endDate={}&sortKind={}&querytype={}&_{}'.format(
            endpoint, 
            startDate,endDate,sortKind,querytype,
            timestamp)
        self.req = requests.session()
        self.data = []

    def get_data(self):
        try:
            response = self.req.get(self.query_url,headers={'Accept-Language': 'zh-TW'})
            content = json.loads(response.text)
            if response.status_code != 200:
                raise CrawlRuntimeError('code: {}\n{}\ncontent: {}'.format(response.status_code,self.query_url,content))
        except Exception as err:
            print('[WarningStock][get_data] {}'.format(err))
            self.data = []
        else:
            self.data = [(data[1],data[2]) for data in content['data']]

        return self.data

    def update_csv(self, input_path):
        """ This function just for test """
        with open(input_path, 'w', newline='') as update_file:
            for data in self.data:        
                writer = csv.writer(update_file, delimiter=',')
                writer.writerow([data[0]])
