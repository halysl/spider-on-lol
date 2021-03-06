# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 对应LOL-Hero-Name
class LOLHeroNameSpiderItem(scrapy.Item):
    '''继承自scrapy.Item，在spiders/lol-hero-name-spidder.py中使用'''
    # name英雄名称，e_name英雄英文名称（即英雄id），title英雄称号
    hero_name = scrapy.Field()
    hero_e_name = scrapy.Field()
    hero_title = scrapy.Field()


# 对应LOL-Item-Name
class LOLItemNameSpiderItem(scrapy.Item):
    # item_id物品id，item_name物品名称
    item_id = scrapy.Field()
    item_name = scrapy.Field()    
    # item_price = scrapy.Field()  # price留坑
    

# 对应LOL-Item-Pic
class LOLItemPicSpiderItem(scrapy.Item):
    # image_urls图片链接
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()


# 对应LOL-Hero-Avatar
class LOLHeroAvatarSpiderItem(scrapy.Item):
    # image_urls图片链接
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()


# 对应LOL-Hero-Skin
class LOLHeroSkinSpiderItem(scrapy.Item):
    # image_urls图片链接，image_names图片名称，image_id图片保存名称
    image_urls = scrapy.Field()
    image_names = scrapy.Field()
    image_id = scrapy.Field()


# 对应LOL-Hero-Story
class LOLHeroStorySpiderItem(scrapy.Item):
    # hero_name英雄名称，hero_story英雄背景故事
    hero_name = scrapy.Field()
    hero_story = scrapy.Field()