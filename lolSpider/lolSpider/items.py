# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LOLHeroNameSpiderItem(scrapy.Item):
    '''继承自scrapy.Item，在spiders/lol-hero-name-spidder.py中使用'''
    # name英雄名称，e_name英雄英文名称（即英雄id），title英雄称号
    hero_name = scrapy.Field()
    hero_e_name = scrapy.Field()
    hero_title = scrapy.Field()

class LOLItemNameSpiderItem(scrapy.Item):
    # item_id物品id，item_name物品名称
    item_id = scrapy.Field()
    item_name = scrapy.Field()
    # price留坑
    # item_price = scrapy.Field()
    

class LOLItemPicSpiderItem(scrapy.Item):
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()

class LOLHeroAvatarSpiderItem(scrapy.Item):
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()
