# -*- coding:utf-8 -*-
import sys
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

from lolSpider.items import LOLHeroSkinSpiderItem


class LOLHeroSkinSpider(scrapy.Spider):
    '''第五个爬虫类，爬取所有英雄皮肤'''
    name = 'LOL-Hero-Skin'
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLHeroSkinPipeline': 300,
            'lolSpider.pipelines.LOLHeroSkinInfoPipeline':301,
        },
        'IMAGES_STORE':'../lolSpider/lolSpider/img/hero_skin_img',
    }
    # 从英雄列表中获取英文名，构造start_urls
    start_urls = []    
    base_url = "http://lol.qq.com/web201310/info-defail.shtml?id="
    with open('./lol-hero-name.json','r') as f:
        for line in f.readlines():            
            i = line.find("e_name") +10
            suf_url = line[i:-3]
            start_urls.append(base_url+suf_url)

    # http header    
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'http://lol.qq.com/web201310/info-defail.shtml?id=Aatrox',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5},
                endpoint='render.html'
            )

    def parse(self,response):
        text = response.xpath("//*[@id=\"skinNAV\"]/li")
        for i in text:
            item = LOLHeroSkinSpiderItem()
            # 获得图片id，为了进一步的重命名
            item["image_id"] = i.xpath("a/img/@src").extract_first().split("/")[-1].replace("small","big")
            # 动态页面，无法抓取到bigxxx.jpg，但可以通过replace构造完整url
            image_urls = i.xpath("a/img/@src").extract_first()
            image_urls = image_urls.replace("small","big")
            temp = []
            temp.append(image_urls)
            item["image_urls"] = temp
            # 皮肤的中文名称，若为“默认”，则添加英雄名称            
            image_names = i.xpath("a/@title").extract_first() 
            if image_names == "默认皮肤":
                item['image_names'] = image_names + " " + response.xpath("//*[@id=\"DATAnametitle\"]/text()").extract_first().split(' ')[-1]
            else:
                item['image_names'] = image_names
            
            yield item