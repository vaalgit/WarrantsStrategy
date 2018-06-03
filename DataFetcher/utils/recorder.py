import os,sys
import csv
from datetime import date

class Recorder(object):
    '''Record data to csv'''
    def __init__(self, path):
        self.folder_path = '{}/{}'.format(path, date.today().strftime('%Y%m%d'))
        if not os.path.isdir(self.folder_path):
            os.mkdir(self.folder_path)

    # Child classes can override this method
    def record_to_csv(self, data):
        pass