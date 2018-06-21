#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import csv
import time

from DataFetcher.utils.errors import CrawlRuntimeError
from DataFetcher.utils.recorder import Recorder
from datetime import date

import requests

class CrawlerController(object):
    '''Split targets into several Crawler, avoid request url too long'''

    def __init__(self, targets, max_stock_per_crawler=50, delay_get_ms=500):
        self.crawlers = []
        self.len = len(targets)
        self.delay_get = delay_get_ms/1000.0        # for delay 500ms
        for index in range(0, self.len ):
            crawler = Crawler([targets[index]])
            self.crawlers.append(crawler)

    def run(self):
        data = []
        for crawler in self.crawlers:
            time.sleep(self.delay_get)
            data.extend(crawler.get_data())
        return data

class Crawler(object):
    '''Request to Market Information System'''
    def __init__(self, targets):
        endpoint = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp'
        # Add 1000 seconds for prevent time inaccuracy
        timestamp = int(time.time() * 1000 + 1000000)
        channels = '|'.join('tse_{}.tw'.format(target) for target in targets)
        self.query_url = '{}?_={}&ex_ch={}'.format(endpoint, timestamp, channels)

        # Get original page to get session
        self.req = requests.session()
        self.req.get('http://mis.twse.com.tw/stock/index.jsp',
                headers={'Accept-Language': 'zh-TW'})

    def get_data(self):
        try:
            response = self.req.get(self.query_url)
            content = json.loads(response.text)
            if response.status_code != 200 or 'msgArray' not in content:
                raise CrawlRuntimeError('code: {}\n{}\ncontent: {}'.format(response.status_code,self.query_url,content))
        except Exception as err:
            print('[Crawler][get_data] {}'.format(err))
            data = []
        else:
            data = content['msgArray']

        return data

class CrawlRecorder(Recorder):
    '''Record data to csv'''
    def __init__(self, path='../Result/data'):
        Recorder.__init__(self,path)

    def record_to_csv(self, data):
        for row in data:
            try:
                file_path = '{}/{}.csv'.format(self.folder_path, row['c'])
                with open(file_path, 'a', newline='') as output_file:
                    writer = csv.writer(output_file, delimiter=',')
                    writer.writerow([
                        row['t'],# 資料時間
                        row['z'],# 最近成交價
                        row['tv'],# 當盤成交量
                        row['v'],# 當日累計成交量
                        row['a'],# 最佳五檔賣出價格
                        row['f'],# 最價五檔賣出數量
                        row['b'],# 最佳五檔買入價格
                        row['g']# 最佳五檔買入數量
                    ])

            except Exception as err:
                print(err)

def main(input_path = None, output_path=None):
    if not input_path:
        input_path = "stocknumber.csv"
    if not output_path:
        output_path = ''

    targets = [_.strip() for _ in open(input_path, 'r')]

    controller = CrawlerController(targets)
    data = controller.run()

    recorder = CrawlRecorder(path=output_path)
    recorder.record_to_csv(data)

if __name__ == '__main__':
    main()
