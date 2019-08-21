# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InsuranceCommentItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    stars = scrapy.Field()
    useful = scrapy.Field()
    comments = scrapy.Field()

class InsuranceCommentItem_huize(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    stars = scrapy.Field()
    comments = scrapy.Field()

