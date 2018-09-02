# -*- coding:utf-8 -*-

import os
import requests

from scrapy import log
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest  # 引入splash组件，获取js数据

from lolSpider.items import LOLHeroInfoSpiderItem


class LOLHeroInfoSpider(Spider):
    """
    第一个爬虫类，爬取英雄联盟所有英雄名字及称号
    """
    name = "LOL-Hero-Info"
    # 同一个项目下，多个spider对应不同的pipeline，需要在spider中修改配置，setting.py中不做pipeline配置
    curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(curr_path, 'img', 'hero_avatar_img')
    custom_settings = {
        'ITEM_PIPELINES': {
            'lolSpider.pipelines.LOLHeroInfoPipeline': 300,
            'lolSpider.pipelines.LOLHeroAvatarPipeline': 301,
        },
        'IMAGES_STORE': image_path,
    }

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'http://lol.qq.com/web201310/info-defail.shtml?id=Aatrox',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/52.0.2743.116 Safari/537.36',
    }

    allowed_domains = ["http://lol.qq.com", "http://ossweb-img.qq.com/images/"]  # 允许爬取的网站域
    # 开始爬取的第一条url
    start_urls = ["http://lol.qq.com/web201310/info-heros.shtml"]

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
            item['hero_avatar_image_url'] = [site.xpath('a/img/@src').extract_first()]
            item['hero_avatar_image_name'] = "_".join(site.xpath("a/@title").extract_first().split(" "))
            hero_js = "".join([default_hero_js, item["hero_e_name"], ".js"])
            log.msg(hero_js)

            r = requests.get(hero_js)
            r.encoding = 'utf-8'
            text = r.text
            story = text.split('lore":"')[-1].split('","blurb')[0]
            item['hero_story'] = story.encode('utf-8').decode('unicode_escape')

            yield item
