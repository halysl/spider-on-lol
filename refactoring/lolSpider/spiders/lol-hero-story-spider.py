# -*- coding:utf-8 -*-
import sys
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from lolSpider.items import LOLHeroStorySpiderItem


class LOLHeroSkinSpider(scrapy.Spider):
    '''第六个爬虫类，爬取英雄的背景故事'''
    name = 'LOL-Hero-Story'
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLHeroStoryPipeline': 300,            
        },
    }
    # 从英雄列表中获取英文名，构造start_urls
    start_urls = []    
    base_url = "http://lol.qq.com/biz/hero/"
    with open('./lol-hero-name.json','r') as f:
        for line in f.readlines():            
            i = line.find("e_name") +10
            suf_url = line[i:-3]
            start_urls.append(base_url+suf_url+".js")

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
        # 获得response的url属性，切分获得英雄名称
        name = response.url.split("/")[-1][:-3]
        # 直接对response内容进行查找，切片，替换等操作取得正确的故事内容        
        story = response.text
        start_index = story.find('\"lore\"')
        end_index = story.find('\"blurb\"')
        story = story[start_index + 8:end_index - 2]
        story = story.replace("<br>","")
        story = story.encode('utf-8').decode('unicode_escape')
        # 添加到item中        
        item = LOLHeroStorySpiderItem()
        item['hero_name'] = name
        item['hero_story'] = story
        yield item