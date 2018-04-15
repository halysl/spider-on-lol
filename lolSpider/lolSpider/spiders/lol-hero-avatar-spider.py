from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from lolSpider.items import LOLHeroAvatarSpiderItem
from scrapy_splash import SplashRequest

class LOLHeroAvatarSpider(Spider):
    '''第三个爬虫类，爬取英雄联盟英雄头像'''
    name = "LOL-Hero-Avatar"
    # 爬虫私有配置，使用scrapy默认的image pipeline
    # 注意IMAGESS_STORE的配置，“../”代表的是scrapy工程的子目录
    custom_settings = {
        'ITEM_PIPELINES':{
            'scrapy.pipelines.images.ImagesPipeline':1,
        },
        'IMAGES_STORE':'../lolSpider/lolSpider/img/hero_avatar_img',
    }
    start_urls = ["http://lol.qq.com/web201310/info-heros.shtml#Navi"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5},
                endpoint='render.html',
            )

    def parse(self, response):
        sites = response.xpath("//*[@id=\"jSearchHeroDiv\"]/li")
        items = []            
        for site in sites:
            item = LOLHeroAvatarSpiderItem()
            # 注意此时使用extract()方法，py3中该方法返回列表，而extract_first()返回bytes
            item["image_urls"] = site.xpath("a/img/@src").extract()
            yield item