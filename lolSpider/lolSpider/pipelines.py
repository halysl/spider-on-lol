# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy import log
from scrapy import Request
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class LOLHeroNamePipeline(object):
    '''
    pipelines是对spider爬取到的item进行处理的过程
    关于scrapy的核心架构可参见https://blog.csdn.net/u012150179/article/details/34441655
    '''
    def __init__(self):
        # codecs,python编解码器，以字节写方式打开一个文件，方便后面的转换中文
        # 关于codecs可以查看https://docs.python.org/3/library/codecs.html
        self.file = codecs.open('lol-hero-name.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  # line是str类型
        # 向codecs("wb")打开的文件写入line经过utf-8编码后再经过unicode编码，最后存储的字符是中文
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLItemNamePipeline(object):    
    def __init__(self):
        self.file = codecs.open('lol-item-name.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLHeroSkinInfoPipeline(object):
    '''
    pipelines是对spider爬取到的item进行处理的过程
    关于scrapy的核心架构可参见https://blog.csdn.net/u012150179/article/details/34441655
    '''
    def __init__(self):
        # codecs,python编解码器，以字节写方式打开一个文件，方便后面的转换中文
        # 关于codecs可以查看https://docs.python.org/3/library/codecs.html
        self.file = codecs.open('lol-skin-info.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'  # line是str类型
        # 向codecs("wb")打开的文件写入line经过utf-8编码后再经过unicode编码，最后存储的字符是中文
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item


class LOLHeroSkinPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    #item['image_urls']是我们在item.py中定义的存放图片url的变量，如果定义了别的变量名，注意更换
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item