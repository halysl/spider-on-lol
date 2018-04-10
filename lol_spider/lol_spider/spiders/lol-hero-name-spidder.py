from scrapy.spiders import Spider
from scrapy.selector import Selector

from lol_spider.items import LOLHeroNameSpiderItem

class LOLHeroNameSpider(Spider):
	name = "LOLHeroName"
	allowed_domains = ["http://lol.178.com"]
	start_urls = ["http://lol.178.com/champion/",]

	def parse(self, response):
		sites = response.xpath("//*[@id=\"content\"]/div[1]/div/div[4]/div/div[2]/div/div[2]/div[1]/a")
		items = []
		print(sites)

		for site in sites:
			item = LOLHeroNameSpiderItem()
			item['name'] = site.xpath("span/text()").extract_first()
			item['title'] = site.xpath("strong/text()").extract_first()
			yield {'name':item['name'],'title':item['title']}
			items.append(item)
		return items
