import scrapy

class Hero_name(scrapy.Spider):
    name = 'hero_name'
    start_urls = ['http://lol.duowan.com/s/heroes.html']

    def parse(self, response):
        for hero_name in response.xpath('//div[@class="champion_name"]'):
            print(hero_name.xpath('text()').extract_first())
            yield {'name':hero_name.xpath('text()').extract_first()}
        for hero_chenghao in response.xpath('//span[@class="champion_search_text"]'):
            print(hero_chenghao.xpath('text()').extract_first())
            yield {'chenghao':hero_chenghao.xpath('text()').extract_first()}