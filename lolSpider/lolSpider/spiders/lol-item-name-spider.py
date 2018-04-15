from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from lolSpider.items import LOLItemNameSpiderItem
from scrapy_splash import SplashRequest

class LOLItemNameSpider(Spider):
    '''
    第二个爬虫类，爬取英雄所有物品名字及id
    '''
    name = "LOL-Item-Name"  # 唯一的名字，命令行执行的时候使用
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLItemNamePipeline': 300,
        }
    }
    
    allowed_domains = ["http://lol.qq.com/web201310/info-item.shtml#Navi"]  # 允许爬取的网站域
    start_urls = ["http://lol.qq.com/web201310/info-item.shtml#Navi",]  # 开始爬取的第一条url
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5},
                endpoint='render.html',
            )
    # parse方法用于处理数据，传入一个response对象
    def parse(self, response):
        # 关于parse方法请看lol-hero-name-spider.py内容
        sites = response.xpath("//*[@id=\"jSearchItemDiv\"]/li")
        items = []

        # 对sites的每一个a元素进行循环
        for site in sites:
            item = LOLItemNameSpiderItem()  # item是LOLItemNameSpiderItem的实例，包含2项item_id、item_name
            item['item_id'] = site.xpath("@data-title").extract_first()  
            item['item_name'] = site.xpath("p/text()").extract_first()  
            # yield函数很复杂，在这里可以理解为“不立即结束的return”，当有了yield函数，可以逐项的将数据添加到json文件或csv文件
            yield {'id':item['item_id'],'name':item['item_name']}  
        

        # 新网址内容不需要迭代，暂存以显示“如何换页”
        # 重点，本来这里应该是下一页的地址，然后迭代执行，但该网站的网站结构和页面有连接关系，不同的页面对应的下一页的xpath不同
        # 所以需要更复杂的处理，在这里，为了方便，直接拼接出下一页的后缀
        # urls = [
        #     "/lol/item-list/tag:,/50", "/lol/item-list/tag:,/100", "/lol/item-list/tag:,/150", 
        #     "/lol/item-list/tag:,/200", "/lol/item-list/tag:,/250", "/lol/item-list/tag:,/300", 
        #     "/lol/item-list/tag:,/350", "/lol/item-list/tag:,/400", "/lol/item-list/tag:,/450",
        #     ]
        # 从urls中取数据，拼接成完整的url，然后交回给原函数执行，就会出现如下情况：
        # 先处理完成50项，然后读取下一页，再完成50项，然后读取下一页......
        # for url in urls:
        #     url = "http://db.178.com" + url
        #     yield Request(url, callback=self.parse)