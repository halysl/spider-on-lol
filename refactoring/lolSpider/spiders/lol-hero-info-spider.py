# -*- coding:utf-8 -*-

import re
import json

from scrapy import log
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest  # 引入splash组件，获取js数据

from lolSpider.items import LOLHeroInfoSpiderItem


class LOLHeroInfoSpider(Spider):
    """
    第一个爬虫类，爬取英雄联盟所有英雄名字及称号
    """
    name = "LOL-Hero-Info"  # 唯一的名字，命令行执行的时候使用
    # 同一个项目下，多个spider对应不同的pipeline，需要在spider中修改配置，setting.py中不做pipeline配置
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLHeroInfoPipeline': 300,
            'lolSpider.pipelines.LOLHeroAvatarPipeline': 301,
        },
    }

    allowed_domains = ["http://lol.qq.com"]  # 允许爬取的网站域
    start_urls = ["http://lol.qq.com/web201310/info-heros.shtml"]  # 开始爬取的第一条url
    
    def start_requests(self):
        for url in self.start_urls:
            # 处理start_urls，以splashRequest的方法执行parse方法
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5}, endpoint='render.html',)
    
    # parse方法用于处理数据，传入一个response对象
    def parse(self, response):
        default_hero_js = 'http://lol.qq.com/biz/hero/'
        sites = response.xpath("//*[@id=\"jSearchHeroDiv\"]/li")
        for site in sites:
            item = LOLHeroInfoSpiderItem()
            item['hero_name'] = site.xpath("a/@title").extract_first().split(" ")[1]
            item['hero_title'] = site.xpath("a/@title").extract_first().split(" ")[0]
            item['hero_e_name'] = site.xpath("a/@href").extract_first().split("=")[-1]
            item['hero_detail_url'] = response.urljoin(site.xpath('a/@href').extract_first())
            item['hero_avatar_image_url'] = site.xpath('a/img/@src').extract_first()
            item['hero_avatar_image_name'] = "_".join(site.xpath("a/@title").extract_first().split(" "))
            hero_js = "".join([default_hero_js, item["hero_e_name"], ".js"])
            log.msg(hero_js)
            item['hero_story'] = self.story_request(hero_js)

            yield item

    def story_request(self, hero_js):
        return SplashRequest(url=hero_js, callback=self.parse_story, args={'wait': 0.5}, endpoint='render.html', )

    def parse_story(self, response):
        text = response.text
        story = text.split('"lore": ')[-1].split('"blurb"')[0]
        log.msg(story)
        return story
