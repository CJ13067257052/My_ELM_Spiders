# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from My_ELM_Spider.items import MyELMBusinessItem, \
    MyElmBusinessFoodItem, MyELMBusinessRatingItem, MyELMBusinessOrderItem


class MyElmSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MonGoWritePipeline(object):
    def __init__(self):
        self.db = MongoClient().E_L_M_Item

    def process_item(self, item, spider):
        if isinstance(item, MyELMBusinessItem):
            if self.db['BusinessItem'].insert(dict(item)):
                print('商家信息成功录入')
            else:
                print('丢弃该数据', item)
        elif isinstance(item, MyElmBusinessFoodItem):
            if self.db['BusinessFoodItem'].insert(dict(item)):
                print('商家商品信息成功录入')
            else:
                print('丢弃该数据', item)
        elif isinstance(item, MyELMBusinessRatingItem):
            if self.db['BusinessRatingItem'].insert(dict(item)):
                print('商家评价信息成功录入')
            else:
                print('丢弃该数据', item)
        elif isinstance(item, MyELMBusinessOrderItem):
            if self.db['BusinessOrderItem'].insert(dict(item)):
                print('商家订单信息成功录入')
            else:
                print('丢弃该数据', item)
        else:
            print('无数据录入')
