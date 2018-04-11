# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class LOLHeroNameSpiderPipeline(object):
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


class LOLItemNameSpiderPipeline(object):    
    def __init__(self):
        self.file = codecs.open('lol-item-name.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.encode('utf-8').decode('unicode_escape'))
        return item