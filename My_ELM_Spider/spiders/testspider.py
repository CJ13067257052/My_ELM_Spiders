# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from My_ELM_Spider.items import MyElmBusinessFoodItem, MyELMBusinessRatingItem, MyELMBusinessOrderItem


class TestspiderSpider(scrapy.Spider):
    name = 'testspider'
    name.split()
    allowed_domains = ['www.baidu.me']
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        for i in range(10):
            yield Request(url='https://www.baidu.com', callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.meta)
        """
        if 'proxy' in response.meta:
            print('>>>>>>Proxy: %s >>>>>Status: %s' % (response.meta['proxy'], response.status))
        else:
            print('>>>>>>Proxy:', '没有使用代理', response.status)
        return Request(url='https://www.sogou.com', callback=self.second_parse, dont_filter=True)
        """

    def second_parse(self, response):
        if 'proxy' in response.meta:
            print('>>>>>>The_Second_Proxy: %s >>>>>Status: %s' % (response.meta['proxy'], response.status))
        else:
            print('>>>>>>The_Second_Proxy:', '没有使用代理', response.status)