# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LOLHeroNameSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name英雄名称，title英雄称号
    name = scrapy.Field()
    title = scrapy.Field()
