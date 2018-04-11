from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from lolSpider.items import LOLItemNameSpiderItem

class LOLItemNameSpider(Spider):
    '''
    第二个爬虫类，爬取英熊联盟所有物品名字、合成价及总价
    '''
    name = "LOL-Item-Name"  # 唯一的名字，命令行执行的时候使用
    custom_settings = {
        'ITEM_PIPELINES':{
            'lolSpider.pipelines.LOLItemNameSpiderPipeline': 300,
        }
    }
    
    # allowed_domains = ["http://db.178.com"]  # 允许爬取的网站域
    start_urls = ["http://db.178.com/lol/item-list/tag:,",]  # 开始爬取的第一条url

    # parse方法用于处理数据，传入一个response对象
    def parse(self, response):
        # 关于parse方法请看lol-hero-name-spider.py内容
        sites = response.xpath("//*[@id=\"sub_ctx_list\"]/div/div[2]/table/tbody/tr")
        items = []

        # 对sites的每一个a元素进行循环
        for site in sites:
            item = LOLItemNameSpiderItem()  # item是LOLItemNameSpiderItem的实例，包含三项name、synthetic_price和total_price
            item['name'] = site.xpath("td[2]/a/text()").extract_first()  
            item['synthetic_price'] = site.xpath("td[5]/span/span/text()").extract_first()  
            item['total_price'] = site.xpath("td[6]/span/span/text()").extract_first()
            # yield函数很复杂，在这里可以理解为“不立即结束的return”，当有了yield函数，可以逐项的将数据添加到json文件或csv文件
            yield {'name':item['name'],'synthetic_price':item['synthetic_price'],'total_price':item['total_price']}  
        
        # 重点，本来这里应该是下一页的地址，然后迭代执行，但该网站的网站结构和页面有连接关系，不同的页面对应的下一页的xpath不同
        # 所以需要更复杂的处理，在这里，为了方便，直接拼接出下一页的后缀
        urls = [
            "/lol/item-list/tag:,/50", "/lol/item-list/tag:,/100", "/lol/item-list/tag:,/150", 
            "/lol/item-list/tag:,/200", "/lol/item-list/tag:,/250", "/lol/item-list/tag:,/300", 
            "/lol/item-list/tag:,/350", "/lol/item-list/tag:,/400", "/lol/item-list/tag:,/450",
            ]
        # 从urls中取数据，拼接成完整的url，然后交回给原函数执行，就会出现如下情况：
        # 先处理完成50项，然后读取下一页，再完成50项，然后读取下一页......
        for url in urls:
            url = "http://db.178.com" + url
            yield Request(url, callback=self.parse)