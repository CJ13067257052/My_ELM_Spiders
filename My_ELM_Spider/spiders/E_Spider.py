# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.loader import ItemLoader
from My_ELM_Spider.items import MyELMBusinessItem, \
    MyElmBusinessFoodItem, MyELMBusinessRatingItem, MyELMBusinessOrderItem


class ESpiderSpider(scrapy.Spider):
    name = 'E_Spider'
    allowed_domains = ['www.ele.me']
    start_urls = ['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash='
                  'wmpmm0jdnp2&latitude=29.04823&limit=24&longitude=111.67285&offset=24&terminal=web']

    # 数据存储
    business_id_array = []
    order_count = 0

    def judge_it_successful(self, business_id):
        if business_id in self.business_id_array:
            return False
        else:
            self.business_id_array.append(business_id)
            return True

    def start_requests(self):
            while len(self.business_id_array) < 50:
                yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('>>>:', response.url)
        print('>>>: %s 连接成功' % response.status)
        json_file = json.loads(response.text)
        for item in json_file:
            business_id = item.get('id')
            if self.judge_it_successful(business_id):
                business = ItemLoader(item=MyELMBusinessItem(), response=response)
                business.add_value('business_name', item.get('name'))
                business.add_value('business_address', item.get('address'))
                business.add_value('business_ave_send_time', item.get('order_lead_time'))
                business.add_value('business_for_send_price', item.get('piecewise_agent_fee').get('rules')[0]
                                   .get('price'))
                business.add_value('business_start_send_price', item.get('piecewise_agent_fee')
                                   .get('rules')[0].get('fee'))
                business.add_value('business_judge_grade', item.get('rating'))
                business.add_value('business_phone', item.get('phone'))
                business.add_value('business_open_time', item.get('opening_hours')[0])
                yield business.load_item()
                food_request = Request(url='https://www.ele.me/restapi/shopping/v2/menu?restaurant_id='
                                       + str(business_id)+'&terminal=web', callback=self.second_food_parse,
                                       dont_filter=True)
                food_request.meta['item'] = business.item
                rating_count_request = Request(url='https://www.ele.me/restapi/ugc/v1/restaurant/'
                                       + str(business_id)+'/rating_categories', callback=self.second_rating_count_parse,
                                       dont_filter=True)
                rating_count_request.meta['item'] = business.item
                yield food_request
                yield rating_count_request

    def second_food_parse(self, response):
        item = response.meta['item']
        print('>>>: %s 连接成功' % response.status)
        print('------------------------------------第一层数据爬取已完成-----------------------------------')
        print('----------------------------------开始进行第二层的商品数据爬取-----------------------------------')
        print('>>> 爬取的商家名：', item['business_name'])
        print('>>> 爬取的商家URL: ', response.url)
        count = 0
        json_file = json.loads(response.text.encode('utf-8'))
        for index in json_file:
            for food in index.get('foods'):
                business_food = ItemLoader(item=MyElmBusinessFoodItem(), response=response)
                business_food.add_value('business_food', item['business_name'])
                business_food.add_value('food_name', food.get('name'))
                business_food.add_value('food_rating', food.get('rating'))
                business_food.add_value('food_month_sale', food.get('month_sales'))
                business_food.add_value('food_recent_rating', food.get('specfoods')[0].get('recent_rating'))
                business_food.add_value('food_price', food.get('specfoods')[0].get('price'))
                business_food.add_value('food_original_price', food.get('specfoods')[0].get('original_price'))
                yield business_food.load_item()
                count += 1
        print('----------成功抓取 %d 商品----------' % count)
        print('----------------------------------#######################-----------------------------------\n')

    def second_rating_count_parse(self, response):
        item = response.meta['item']
        print('>>>: %s 连接成功' % response.status)
        json_file = json.loads(response.text.encode('utf-8'))
        print('----------------------------------开始进行第二层的评价数据爬取----------------------------')
        print('>>> 爬取的商家名：', item['business_name'])
        print('>>> 爬取的商家URL: ', response.url)
        business_rating = ItemLoader(item=MyELMBusinessRatingItem(), response=response)
        business_rating.add_value('business_name', item['business_name'])
        business_rating.add_value('good_rating', json_file[1].get('amount'))
        business_rating.add_value('bad_rating', json_file[2].get('amount'))
        business_rating.add_value('total_rating', json_file[0].get('amount'))
        yield business_rating.load_item()
        for index in range(0, business_rating.item['total_rating'], 10):
            request = Request(url='https://www.ele.me/restapi/ugc/v1/restaurant/161357954/ratings?limit=10&offset='
                              + str(index) + '&record_type=1',
                              callback=self.second_order_parse, dont_filter=True)
            request.meta['item'] = item
            yield request

    def second_order_parse(self, response):
        print('----------------------------------开始进行第二层的评价订单爬取----------------------------')
        json_file = json.loads(response.text.encode('utf-8'))
        for rating in json_file:
            customer_order = ItemLoader(item=MyELMBusinessOrderItem(), response=response)
            customer_order.add_value('business_name', response.meta['item']['business_name'])
            customer_order.add_value('customer_order_time', rating.get('rated_at'))
            for index in rating.get('item_rating_list'):
                customer_order.add_value('customer_order', index.get('rate_name'))
            yield customer_order.load_item()
            self.order_count += 1
        print('----------------------------------------抓取到%d条订单数据------------------------------\n' % self.order_count)

