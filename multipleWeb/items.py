# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class yingjieshengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    body = scrapy.Field()



class nwpujobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()  # 标题
    company = scrapy.Field()  # 单位名称
    company_property = scrapy.Field()#单位性质
    industry = scrapy.Field()
    location = scrapy.Field()
    body = scrapy.Field()