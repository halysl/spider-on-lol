* v1.0为爬虫早期版本，详细内容请看v1.0/README.md
* lol_spider为全程使用scrapy框架，添加必要说明，完善内部逻辑。
* 爬虫主要爬取的网站是lol.qq.com
* 现提供爬虫如下：

|         爬虫          |             使用方法             | 说明              |
| :-----------------: | :--------------------------: | --------------- |
|  LOLHeroNameSpider  |  scrapy crawl LOL-Hero-Name  | 获取英雄名称，返回json   |
|  LOLItemNameSpider  |  scrapy crawl LOL-Item-Name  | 获取物品名称，返回json   |
|  LOLItemPicSpider   |  scrapy crawl LOL-Item-Pic   | 获取物品名称，下载jpg文件  |
| LOLHeroAvatarSpider | scrapy crawl LOL-Hero-Avatar | 获取英雄头像，下载jpg 文件 |
|  LOLHeroSkinSpider  |  scrapy crawl LOL-Hero-Skin  | 获取英雄皮肤，下载jpg 文件 |
|  LOLHeroSkinSpider  | scrapy crawl LOL-Hero-Story  | 获取英雄背景故事，返回json |
* 为了处理js，使用了splash
* 具体实现过程参考loSpider/lolSpider/spiders