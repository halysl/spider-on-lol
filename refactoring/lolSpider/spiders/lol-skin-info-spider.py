# -*- coding:utf-8 -*-

import os
import re
import json

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
    # 开始爬取的第一条url
    start_urls = ["http://lol.qq.com/web201310/info-heros.shtml"]