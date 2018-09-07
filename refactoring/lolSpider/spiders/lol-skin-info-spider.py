# -*- coding:utf-8 -*-

import os
import json

from scrapy import log
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest  # 引入splash组件，获取js数据

from lolSpider.items import LOLSkinInfoSpiderItem


class LOLSkinInfoSpider(Spider):
    name = "LOL-Skin-Info"
    curr_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    image_path = os.path.join(curr_path, 'img', 'skin_img')
    custom_settings = {
        'ITEM_PIPELINES': {
            'lolSpider.pipelines.LOLSkinInfoPipeline': 300,
            'lolSpider.pipelines.LOLSkinImgPipeline': 301,
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

    data = []
    start_urls = []
    with open('lol-hero-info.json', 'r') as f:
        for line in f.readlines():
            start_urls.append(json.loads(line)['hero_detail_url'])

    def start_requests(self):
        for url in self.start_urls:
            log.msg(url)
            # 处理start_urls，以splashRequest的方法执行parse方法
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5}, endpoint='render.html')

    def parse(self, response):
        skins = response.xpath('//*[@id="skinBG"]/li')
        for skin in skins:
            item = LOLSkinInfoSpiderItem()
            item['image_urls'] = ["".join(['http:', skin.xpath('img/@src').extract_first()])]
            item['image_id'] = skin.xpath('img/@src').extract_first().split('big')[-1].split('.jpg')[0]
            image_names = skin.xpath("@title").extract_first()
            if image_names == "默认皮肤":
                item['image_names'] = image_names + " " + response.xpath("//*[@id=\"DATAnametitle\"]/text()").extract_first().split(' ')[-1]
            else:
                item['image_names'] = image_names
            log.msg(item)

            yield item
