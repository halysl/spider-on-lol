# -*- coding:utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from lolSpider.items import LOLItemPicSpiderItem


class LOLItemPicSpider(Spider):
    '''第三个爬虫类，爬取英雄联盟物品图片'''
    name = "LOL-Item-Pic"
    # 爬虫私有配置，使用scrapy默认的image pipeline
    # 注意IMAGESS_STORE的配置，“../”代表的是scrapy工程的子目录
    custom_settings = {
        'ITEM_PIPELINES':{
            'scrapy.pipelines.images.ImagesPipeline':1,
        },
        'IMAGES_STORE':'../lolSpider/lolSpider/img/item_img',
    }
    start_urls = ["http://lol.qq.com/web201310/info-item.shtml#Navi",]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5},
                endpoint='render.html',
            )

    def parse(self, response):
        sites = response.xpath("//*[@id=\"jSearchItemDiv\"]/li")
        items = []            
        for site in sites:
            item = LOLItemPicSpiderItem()
            # 注意此时使用extract()方法，py3中该方法返回列表，而extract_first()返回bytes
            item["image_urls"] = site.xpath("img/@src").extract()
            yield item