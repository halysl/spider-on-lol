# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LOLHeroInfoSpiderItem(scrapy.Item):
    """
    继承自scrapy.Item，在spiders/lol-hero-info-spider.py中使用
    """
    # name英雄名称，e_name英雄英文名称（即英雄id），title英雄称号
    hero_detail_url = scrapy.Field()
    hero_name = scrapy.Field()
    hero_e_name = scrapy.Field()
    hero_title = scrapy.Field()
    hero_story = scrapy.Field()
    hero_avatar_image_url = scrapy.Field()
    hero_avatar_image_name = scrapy.Field()


# 对应LOL-Item-Name
class LOLItemInfoSpiderItem(scrapy.Item):
    item_id = scrapy.Field()
    item_name = scrapy.Field()
    # 物品功能描述
    item_func = scrapy.Field()
    # 物品简介
    item_desc = scrapy.Field()
    # price is a dict,include base purchasable total sell
    item_price = scrapy.Field()
    item_tag = scrapy.Field()
    item_image_url = scrapy.Field()


class LOLSkinInfoSpiderItem(scrapy.Item):
    # image_urls图片链接，image_names图片名称，image_id图片保存名称
    image_urls = scrapy.Field()
    image_names = scrapy.Field()
    image_id = scrapy.Field()
