# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class LOLHeroInfoPipeline(object):
    """
    lol英雄基本信息采集
    """
    def __init__(self):
        # 关于codecs可以查看https://docs.python.org/3/library/codecs.html
        self.file = codecs.open('lol-hero-info.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  # line是str类型
        # 向codecs("wb")打开的文件写入line经过utf-8编码后再经过unicode编码，最后存储的字符是中文
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLHeroAvatarPipeline(ImagesPipeline):
    """
    lol英雄头像采集
    """
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % image_guid

    def get_media_requests(self, item, info):
        for image_url in item['hero_avatar_image_url']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class LOLItemInfoPipeline(object):
    """
    lol物品基本信息采集
    """
    def __init__(self):
        self.file = codecs.open('lol-item-info.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLItemImgPipeline(ImagesPipeline):
    """
    lol物品图像采集
    """
    def get_media_requests(self, item, info):
        for image_url in item['item_image_url']:
            yield Request(image_url, meta={'item_name':item['item_name']})

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta['item_name']
        return 'full/%s.jpg' % image_guid

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


class LOLSkinInfoPipeline(object):
    """
    lol皮肤基本信息采集
    """
    def __init__(self):
        # codecs,python编解码器，以字节写方式打开一个文件，方便后面的转换中文
        # 关于codecs可以查看https://docs.python.org/3/library/codecs.html
        self.file = codecs.open('lol-skin-info.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  # line是str类型
        # 向codecs("wb")打开的文件写入line经过utf-8编码后再经过unicode编码，最后存储的字符是中文
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLSkinImgPipeline(ImagesPipeline):
    """
    lol皮肤图片采集
    """

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'image_name': item['image_names']})

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta['image_name']
        return 'full/%s.jpg' % image_guid

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
