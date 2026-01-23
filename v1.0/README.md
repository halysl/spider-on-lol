# Spider-on-LOL v1.0 🎮

> 英雄联盟数据爬虫的早期版本

## 📖 简介

这是 `spider-on-lol` 项目的 **v1.0 版本**，使用 Python 原生库编写的爬虫脚本，用于从 [lol.qq.com](https://lol.qq.com) 爬取英雄头像、皮肤原画、装备图片及英雄故事。

本版本采用最基础的爬虫方式：通过 `requests` 发送 HTTP 请求，使用 `BeautifulSoup` 解析 HTML，利用 `PIL` 处理图片下载。适合爬虫初学者学习和理解爬虫的基本原理。

## 🛠️ 技术栈

| 库 | 用途 |
|:---:|:---|
| `requests` | HTTP 请求，获取网页内容 |
| `BeautifulSoup4` | HTML 解析，提取数据 |
| `Scrapy` | 部分脚本使用 Scrapy 框架 |
| `PIL/Pillow` | 图片处理与保存 |
| `io` | 处理二进制图片流 |

## 📁 文件说明

### 数据源文件

| 文件 | 说明 |
|:---:|:---|
| `name.txt` | 英雄英文名数据源，从某网站获取，用于早期爬虫构建URL |
| `dict.py` | 处理 `name.txt` 的辅助脚本，解析英雄名称数据 |

### 爬虫脚本

| 文件 | 技术方案 | 功能说明 |
|:---:|:---:|:---|
| `lol_hero_name.py` | Scrapy + XPath | 爬取英雄称号及英雄名，输出 JSON 文件 |
| `lol_pic.py` | requests + PIL | 批量下载英雄头像图片 |
| `lol_hero_story.py` | requests + BeautifulSoup | 爬取英雄背景故事，解析 JS 文件获取中文文本 |
| `lol_item_image.py` | requests + PIL | 暴力遍历指定范围URL，下载物品图片 |
| `lol_skin_image.py` | requests + PIL | 构建合理URL范围，判断存在后下载皮肤原画 |
| `test.py` | - | 临时测试文件 |

### 输出文件

| 文件/目录 | 说明 |
|:---:|:---|
| `lol_hero_name.json` | `lol_hero_name.py` 生成的英雄名称数据 |
| `hero_story/` | 存放英雄背景故事文本文件（约70个英雄） |
| `pic/hero/` | 存放英雄头像图片 |
| `pic/item/` | 存放装备物品图片 |
| `pic/skin/` | 存放皮肤原画图片 |

## 🔍 爬虫实现详解

### 1. 英雄名称爬取 (`lol_hero_name.py`)

使用 Scrapy 框架，通过 XPath 定位页面元素：

```python
import scrapy

class Hero_name(scrapy.Spider):
    name = 'hero_name'
    start_urls = ['http://lol.duowan.com/s/heroes.html']

    def parse(self, response):
        for hero_name in response.xpath('//div[@class="champion_name"]'):
            yield {'name': hero_name.xpath('text()').extract_first()}
```

**关键点：**
- 使用 XPath `//div[@class="champion_name"]` 定位英雄名称元素
- 使用 `extract_first()` 提取第一个匹配的文本内容
- 使用 `yield` 逐条输出数据

### 2. 英雄头像下载 (`lol_pic.py`)

直接构建图片URL，使用 requests 下载：

```python
import requests
from PIL import Image
from io import BytesIO

def getdata(li):
    for name in li:
        url = f'http://ossweb-img.qq.com/images/lol/img/champion/{name}.png'
        r = requests.get(url)
        image = Image.open(BytesIO(r.content))
        image.save(f'pic/hero/{name}.png')
```

**关键点：**
- 分析网站图片URL规律：`/images/lol/img/champion/{英雄英文名}.png`
- 使用 `BytesIO` 处理二进制图片数据流
- 使用 PIL 的 `Image.save()` 保存图片

### 3. 英雄故事爬取 (`lol_hero_story.py`)

从 JS 文件中提取故事文本：

```python
import requests
from bs4 import BeautifulSoup

def lol_hero_story(hero_name):
    for name in hero_name:
        url = f'http://lol.qq.com/biz/hero/{name}.js'
        r = requests.get(url)
        r.encoding = 'utf-8'
        
        # 从JS中提取lore字段
        start = demo.find('lore')
        end = demo.find('blurb')
        story = demo[start:end][7:-3]
        
        # Unicode转中文
        story = story.encode('utf-8').decode('unicode_escape')
```

**关键点：**
- 英雄故事存储在 JS 文件中，格式为 `lore":"故事内容"`
- 需要处理 Unicode 转义字符，转换为中文
- 清除 HTML 标签如 `<br>`

### 4. 物品图片下载 (`lol_item_image.py`)

暴力遍历URL范围：

```python
def lol_item_img():
    for i in range(2000, 4000):
        url = f'http://ossweb-img.qq.com/images/lol/img/item/{i}.png'
        r = requests.get(url)
        if r.status_code == 200:  # 判断图片是否存在
            img = Image.open(BytesIO(r.content))
            img.save(f'pic/item/{i}.png')
        time.sleep(0.1)  # 控制请求频率
```

**关键点：**
- 物品ID在 2000-4000 范围内
- 通过 HTTP 状态码判断图片是否存在
- 添加 `time.sleep()` 控制请求频率，避免被封

### 5. 皮肤原画下载 (`lol_skin_image.py`)

构建合理的URL范围：

```python
def lol_skin_image():
    for hero_id in range(1, 123):
        for skin_id in range(20):
            # URL格式: big{英雄ID}{皮肤ID}.jpg
            skin_num = f"00{skin_id}" if skin_id < 10 else f"0{skin_id}"
            url = f'http://ossweb-img.qq.com/images/lol/web201310/skin/big{hero_id}{skin_num}.jpg'
            
            r = requests.get(url)
            if r.status_code == 200:
                img = Image.open(BytesIO(r.content))
                img.save(f'pic/skin/{hero_id}/{skin_id}.jpg')
```

**关键点：**
- 英雄ID范围：1-122
- 每个英雄最多约20个皮肤
- 皮肤URL格式需要补零：`000`, `001`, ..., `019`

## 📊 数据输出示例

### lol_hero_name.json

```json
[
    {"name": "黑暗之女", "chenghao": "安妮"},
    {"name": "狂战士", "chenghao": "奥拉夫"},
    {"name": "正义巨像", "chenghao": "加里奥"}
]
```

### hero_story/Annie.txt

```
在诺克萨斯帝国偏远的北部边境，有一个地势险要的山区，每家每户门口都挂着护身符，
以求驱逐那些可能释放到人间的恶灵。在这些高耸入云的群山之中...
```

## ⚠️ 注意事项

1. **路径配置**：脚本中包含硬编码的本地路径，使用前需要修改为自己的路径
2. **请求频率**：建议添加适当的延时，避免请求过于频繁
3. **网站变化**：此版本基于 2018 年的网站结构，目标网站可能已更新
4. **仅供学习**：本项目仅用于学习爬虫技术

## 🔄 后续版本

本版本之后，项目引入了 Scrapy 框架进行重构：

- **v2.0** (`lolSpider/`)：完整使用 Scrapy + Splash 框架
- **refactoring** (`refactoring/`)：进一步优化，使用 ImagePipeline

请查看 [主 README](../README.md) 了解更多版本信息。

## 📝 学习要点

通过这个版本，你可以学习到：

1. **HTTP 请求**：使用 requests 库发送 GET 请求
2. **HTML 解析**：使用 BeautifulSoup 和 XPath 提取数据
3. **图片处理**：使用 PIL 处理和保存图片
4. **数据提取**：从 JavaScript 文件中提取结构化数据
5. **爬虫策略**：URL 规律分析、暴力遍历、存在性判断

---

> 💡 *这是一个很好的爬虫入门项目，代码简单直观，适合理解爬虫的核心原理。*
