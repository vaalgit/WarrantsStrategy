#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import re

from DataFetcher.utils.recorder import Recorder
from datetime import date

import requests

''' Actually don't know what it is '''
class NDAYS_SV:
    sv_1 = '60'

''' Actually don't know what it is '''
class HISTV:
    v_1 = '60'

class DNAME:
    name_1 = '%u7FA4%u76CA%u91D1%u9F0E' #群益金鼎

class CrawlerController(object):
    '''Split targets into several Crawler, avoid request url too long'''
    def __init__(self, targets, max_stock_per_crawler=50):
        self.session = SessionKeeper()
        self.crawlers = []
        self.len = len(targets)
        for index in range(0, self.len):
            token = TokenFinder(targets[index], self.session.get_session())
            crawler = Crawler(token.get_token(), self.session.get_session())
            self.crawlers.append(crawler)

    def run(self):
        data = []
        for crawler in self.crawlers:
            data.append(crawler.get_data())
        return data

class SessionKeeper(object):
    '''Store iwarrant http session'''
    def __init__(self):
        # Get original page to get session
        self.sess = requests.session()
        self.sess.get('http://iwarrant.capital.com.tw/warrants/wScreenerPull.aspx',
                headers={'Accept-Language': 'zh-TW'})

    def get_session(self):
        return self.sess

class TokenFinder(object):
    '''Request to Market Information System'''
    def __init__(self, target, session):
        endpoint = 'http://iwarrant.capital.com.tw/warrants/data/Get_wScreenerResultScodes.aspx'
        # Add 1000 seconds for prevent time inaccuracy
        timestamp = int(time.time() * 1000 + 1000000)
        self.query_url = '{}?dname={}&ul={}&histv={}&_={}'.format(
            endpoint,
            DNAME.name_1,
            target ,
            HISTV.v_1,
            timestamp)
        self.session = session

    def get_token(self):
        try:
            response = self.session.get(self.query_url)
            pattern = r"\|.*\|$" #Search for "|yyyy/mm/dd hh:mm:ss|" in the end of string
            context = re.sub(pattern, '', response.text)
        except Exception as err:
            print('[get_token] {}'.format(err))
            token = ''
        else:
            token = context
        
        return token

class Crawler(object):
    '''Get information result by tokens'''
    def __init__(self, token, session):
        endpoint = 'http://iwarrant.capital.com.tw/warrants/data/getWantUnFloatTerms.aspx'
        # Add 1000 seconds for prevent time inaccuracy
        timestamp = int(time.time() * 1000 + 1000000)
        self.query_url = '{}?wcodelist={}&ndays_sv={}&_={}'.format(
            endpoint,
            token,
            NDAYS_SV.sv_1,
            timestamp)
        self.session = session

    def get_data(self):
        try:
            response = self.session.get(self.query_url)
            content = json.loads(response.text)
        except Exception as err:
            print('[get_data] {}'.format(err))
            data = []
        else:
            data = content

        return data

class CrawlRecorder(Recorder):
    '''Record data to csv'''
    def __init__(self, path='../Result/data'):
        Recorder.__init__(self,path)

    def record_to_csv(self, data):
        for company in data:
            infos = company['recs']
            for row in infos:
                try:
                    file_path = '{}/{}.csv'.format(self.folder_path, row['tse_idx_scode'])
                    with open(file_path, 'a') as output_file:
                        writer = csv.writer(output_file, delimiter=',')
                        writer.writerow([
                            row['lst_date'],        #起始時間?
                            row['last_date'],       #結束時間?
                            row['mat_date'],        #?
                            row['scode'],           #權證代號
                            row['sname'],           #權證名稱
                            #row['idx_name'],        #公司名稱
                            #row['scodename'],       #權證代號+權證名稱
                            row['share_rate'],      #行使比例
                            row['days'],            #剩餘天數
                            row['days_trade'],      #已過天數?
                            row['isUlTrade'],       #?  ex:'Y'
                            row['lexprc'],          #?  ex:27
                            row['c_p_type'],        #?  ex:'C'
                            row['l_p_up'],          #?  ex:None
                            row['want_remain_vol'], #?  ex:3500
                            row['oi'],              #?  ex:562
                            row['oir'],             #?  ex:16.06
                            row['risk_free'],       #?  ex:0.0143
                            row['hv']               #?  ex:0.229814
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
