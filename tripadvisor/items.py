# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    content = scrapy.Field()
    rating = scrapy.Field()
    

class RestaurantItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    content = scrapy.Field()
    rating = scrapy.Field()
