from scrapy.spiders import Spider
from scrapy.selector import Selector

from lolSpider.items import LOLHeroNameSpiderItem

class LOLHeroNameSpider(Spider):
	'''
	第一个爬虫类，爬取英熊联盟所有英雄名字及称号
	'''	
	name = "LOL-Hero-Name"  # 唯一的名字，命令行执行的时候使用
	allowed_domains = ["http://lol.178.com"]  # 允许爬取的网站域
	start_urls = ["http://lol.178.com/champion/",]  # 开始爬取的第一条url

	# parse方法用于处理数据，传入一个response对象
	def parse(self, response):
		# sites是一个可迭代对象，它代表了从response对象中获取某些数据而形成的可迭代对象
		# 使用xpath方法找到特定的元素组成的数据，在这里代表“找到一个id为content的元素它的第一个div元素的div元素的第四个div元素的
		# div元素的第二个div元素的div元素的第二个div元素的第一个div元素下的所有a元素”，很多个a元素，所以成为一个可迭代对象
		# XPath是一门在XML、HTML文档中查找信息的语言，它可以查找元素。教程可见http://www.w3school.com.cn/xpath/index.asp
		# 之前的xpath很长，但不需要对着网页源代码查找，请见http://www.locoy.com/Public/guide/V9/HTML/XPath%E6%8F%90%E5%8F%96.html
		sites = response.xpath("//*[@id=\"content\"]/div[1]/div/div[4]/div/div[2]/div/div[2]/div[1]/a")
		items = []

		# 对sites的每一个a元素进行循环
		for site in sites:
			item = LOLHeroNameSpiderItem()  # item是LOLHeroNameSpiderItem的实例，包含两项name和title
			item['name'] = site.xpath("span/text()").extract_first()  # 此处使用xpath的相对定位，将a元素内的span元素的text值给item['name']
			item['title'] = site.xpath("strong/text()").extract_first()  # 此处使用xpath的相对定位，将a元素内的strong元素的text值给item['title']
			# yield函数很复杂，在这里可以理解为“不立即结束的return”，当有了yield函数，可以逐项的将数据添加到json文件或csv文件
			yield {'name':item['name'],'title':item['title']}  
			items.append(item)
		# return 也可以完成yield的任务（在这个文件内），两者都可以输出到json文件（保留一个就好hh）
		return items