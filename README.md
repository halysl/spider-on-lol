# spider-on-lol
用python写爬虫访问lol.qq.com爬取英雄头像、皮肤原画、装备图片及英雄故事

* name.txt：是来自某网站直接英雄名数据，但仅有英文，爬虫中前期使用
* dict.py：处理name.txt的数据
* lol\_hero\_name.py：使用scrapy框架，xpath查找关键词，返回json文件，文件内容包括英雄称号及英雄名
* lol\_hero\_name.json：lol\_hero\_name.py产生的文件
* lol\_pic.py：使用request+bs4爬取内容，io库读取图片内容，PIL库进行下载，批量化下载
* lol\_hero\_story.py：使用request+bs4爬取内容，转换js内容为中文文本
* lol\_item\_image.py：使用request+PIL爬取内容，指定网页范围，暴力爬取
* lol\_skin\_image.py：使用request+PIL爬取内容，观察网页内容，构建一个合理的范围，判断存在再爬取
* test.py：临时测试文件
* ／hero_story：存放英雄故事
* /pic/hero：存放英雄头像
* /pic/item：存放物品图片
* /pic/skin：存放皮肤原画
