# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class JdmaotaoPipeline(object):
    def open_spider(self, spider):
        self.result = pd.DataFrame(columns=['productID','price','shopname', 'name', 'commit','url','info'])

    
    def close_spider(self, spider):
        self.result.to_excel('result.xlsx')
        print ("close")

    def process_item(self, item, spider):
        self.result = self.result.append(dict(item), ignore_index=True)
        return item