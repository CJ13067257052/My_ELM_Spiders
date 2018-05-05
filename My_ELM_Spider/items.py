# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.loader.processors import Compose, TakeFirst, MapCompose


def data_clear(item_filed):
    return item_filed.strip('】').split('【')[0]


class MyELMBusinessItem(scrapy.Item):
    business_name = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_address = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_ave_send_time = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_for_send_price = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_start_send_price = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_judge_grade = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_phone = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    business_open_time = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )


class MyElmBusinessFoodItem(scrapy.Item):
    business_name = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_name = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_rating = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_recent_rating = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_price = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_original_price = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    food_month_sale = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )


class MyELMBusinessRatingItem(scrapy.Item):
    business_name = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    good_rating = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    bad_rating = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    total_rating = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )


class MyELMBusinessOrderItem(scrapy.Item):
    business_name = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )
    customer_order = scrapy.Field(
        output_processor=MapCompose(data_clear)
    )
    customer_order_time = scrapy.Field(
        output_processor=Compose(TakeFirst())
    )