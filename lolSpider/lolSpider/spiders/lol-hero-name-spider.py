# -*- coding:utf-8 -*-
import json
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest  # 引入splash组件，获取js数据

from lolSpider.items import LOLHeroNameSpiderItem


class LOLHeroNameSpider(Spider):
    '''
    第一个爬虫类，爬取英雄联盟所有英雄名字及称号
    '''    
    name = "LOL-Hero-Name"  # 唯一的名字，命令行执行的时候使用
    # 同一个项目下，多个spider对应不同的pipeline，需要在spider中修改配置，setting.py中不做pipeline配置
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLHeroNamePipeline': 300,
        },        
    }

    allowed_domains = ["http://lol.qq.com/web201310/info-heros.shtml"]  # 允许爬取的网站域
    start_urls = ["http://lol.qq.com/web201310/info-heros.shtml",]  # 开始爬取的第一条url
    
    def start_requests(self):
        for url in self.start_urls:
            # 处理start_urls，以splashRequest的方法执行parse方法
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5},
                endpoint='render.html',
            )
    
    # parse方法用于处理数据，传入一个response对象
    def parse(self, response):
        # sites是一个可迭代对象，它代表了从response对象中获取某些数据而形成的可迭代对象
        # 使用xpath方法找到特定的元素组成的数据，在这里代表“找到一个id为jSearchHeroDiv的元素它的所有li元素，很多个li元素，所以成为一个可迭代对象
        # XPath是一门在XML、HTML文档中查找信息的语言，它可以查找元素。教程可见http://www.w3school.com.cn/xpath/index.asp
        # 之前的xpath很长，但不需要对着网页源代码查找，请见http://www.locoy.com/Public/guide/V9/HTML/XPath%E6%8F%90%E5%8F%96.html
        sites = response.xpath("//*[@id=\"jSearchHeroDiv\"]/li")
        items = []

        # 对sites的每一个li元素进行循环
        for site in sites:
            item = LOLHeroNameSpiderItem()  # item是LOLHeroNameSpiderItem的实例，包含两项name和title
            item['hero_name'] = site.xpath("a/@title").extract_first().split(" ")[1]  # 此处使用xpath的相对定位，将li元素内的a元素的title属性值以空格切分取第二项给item['name']
            item['hero_title'] = site.xpath("a/@title").extract_first().split(" ")[0]  # 此处使用xpath的相对定位，将li元素内的a元素的title属性值以空格切分取第一项给item['title']
            item['hero_e_name'] = site.xpath("a/@href").extract_first()[21:]  # 将li元素内的a元素的href取切片[21:]获得英雄的英文名称
            # yield函数很复杂，在这里可以理解为“不立即结束的return”，当有了yield函数，可以逐项的将数据添加到json文件或csv文件
            yield {'name':item['hero_name'],'title':item['hero_title'],"e_name":item['hero_e_name']}  
            items.append(item)
        # return 也可以完成yield的任务（在这个文件内），两者都可以输出到json文件（保留一个就好hh）
        return items