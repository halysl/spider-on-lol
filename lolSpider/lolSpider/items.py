# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LOLHeroNameSpiderItem(scrapy.Item):
    '''继承自scrapy.Item，在spiders/lol-hero-name-spidder.py中使用'''
    # name英雄名称，title英雄称号
    name = scrapy.Field()
    title = scrapy.Field()