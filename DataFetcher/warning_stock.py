import time
import json
import requests
from datetime import datetime
from crawl import Recorder
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

    def get_data(self):
        try:
            response = self.req.get(self.query_url,headers={'Accept-Language': 'zh-TW'})
            content = json.loads(response.text)
        except Exception as err:
            print('[get_data] {}'.format(err))
            data = []
        else:
            data = content['msgArray']

        return data