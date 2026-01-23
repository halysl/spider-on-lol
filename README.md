# Spider-on-LOL 🎮

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.6+-green.svg)](https://scrapy.org/)

> 一个用于爬取英雄联盟（LOL）官方网站数据的 Python 爬虫项目

## 📖 项目简介

本项目创建于 **2018 年**，主要目的是从 [lol.qq.com](https://lol.qq.com) 爬取英雄联盟相关数据，包括：

- 🦸 英雄名称与称号
- 📜 英雄背景故事
- 🖼️ 英雄头像图片
- 🎨 英雄皮肤原画
- ⚔️ 装备物品信息及图片

## 🚀 版本演进

本项目经历了多次迭代重构，从最初的简单脚本逐步演进为基于 Scrapy 框架的完整爬虫系统：

| 版本 | 目录 | 技术栈 | 说明 |
|:---:|:---:|:---:|:---|
| **v1.0** | `v1.0/` | requests + BeautifulSoup + PIL | 早期版本，使用原生请求库 |
| **v1.1 - v1.5** | - | scrapy 初步引入 | 过渡版本，开始使用scrapy框架 |
| **v2.0** | `lolSpider/` | Scrapy + Splash | 完整框架重写，支持JS渲染 |
| **refactoring** | `refactoring/` | Scrapy + Splash + ImagePipeline | 重构版本，完善数据采集流程 |

### v1.0 - 原始版本

使用 `requests`、`BeautifulSoup`、`PIL` 等基础库，通过直接发送 HTTP 请求获取数据。详细信息请查看 [v1.0/README.md](./v1.0/README.md)。

**特点：**
- 简单直接的脚本方式
- 使用 XPath 和 CSS 选择器解析HTML
- 手动处理图片下载和保存

### v2.0 - Scrapy 框架重写

完全使用 Scrapy 框架重写，引入 Splash 组件处理 JavaScript 渲染的页面。

**特点：**
- 使用 Scrapy 的标准项目结构
- 通过 Splash 处理动态加载内容
- 使用 Pipeline 分离数据处理逻辑
- 支持多个独立的 Spider

### refactoring - 重构优化版

在 v2.0 基础上进一步重构，整合数据采集流程，增加图片下载管道。

**特点：**
- 使用 ImagePipeline 自动管理图片下载
- 优化代码结构和复用性
- 完善英雄信息、物品信息、皮肤图片采集

## 📁 项目结构

```
spider-on-lol/
├── README.md                 # 本文件
├── Pipfile                   # Python 依赖管理
├── Pipfile.lock              
├── v1.0/                     # v1.0 早期版本
│   ├── README.md             # v1.0 详细说明
│   ├── lol_hero_name.py      # 英雄名称爬取
│   ├── lol_hero_story.py     # 英雄故事爬取
│   ├── lol_pic.py            # 英雄头像爬取
│   ├── lol_item_image.py     # 物品图片爬取
│   ├── lol_skin_image.py     # 皮肤原画爬取
│   ├── hero_story/           # 英雄故事存储目录
│   └── pic/                  # 图片存储目录
├── lolSpider/                # v2.0 Scrapy 版本
│   ├── scrapy.cfg            
│   └── lolSpider/            
│       ├── items.py          # 数据模型定义
│       ├── pipelines.py      # 数据处理管道
│       ├── settings.py       # Scrapy 配置
│       └── spiders/          # 爬虫定义
│           ├── lol-hero-name-spider.py
│           ├── lol-hero-avatar-spider.py
│           ├── lol-hero-skin-spider.py
│           ├── lol-hero-story-spider.py
│           ├── lol-item-name-spider.py
│           └── lol-item-pic-spider.py
└── refactoring/              # 重构版本
    ├── scrapy.cfg            
    └── lolSpider/            
        ├── items.py
        ├── pipelines.py
        ├── settings.py
        ├── img/              # 图片存储目录
        └── spiders/
            ├── lol-hero-info-spider.py
            ├── lol-item-info-spider.py
            └── lol-skin-info-spider.py
```

## ⚙️ 环境配置

### 依赖安装

使用 Pipenv 管理依赖：

```bash
# 安装 pipenv（如果尚未安装）
pip install pipenv

# 安装项目依赖
pipenv install

# 激活虚拟环境
pipenv shell
```

### Splash 配置

本项目使用 Splash 处理 JavaScript 渲染，需要先启动 Splash 服务：

```bash
# 使用 Docker 启动 Splash
docker run -p 8050:8050 scrapinghub/splash
```

## 🕷️ 使用方法

### v2.0 版本（推荐）

进入 `lolSpider` 目录，使用 Scrapy 命令运行爬虫：

```bash
cd lolSpider

# 获取英雄名称
scrapy crawl LOL-Hero-Name

# 获取物品名称
scrapy crawl LOL-Item-Name

# 获取物品图片
scrapy crawl LOL-Item-Pic

# 获取英雄头像
scrapy crawl LOL-Hero-Avatar

# 获取英雄皮肤
scrapy crawl LOL-Hero-Skin

# 获取英雄背景故事
scrapy crawl LOL-Hero-Story
```

### 爬虫列表

| 爬虫名称 | 运行命令 | 说明 |
|:---:|:---:|:---|
| LOLHeroNameSpider | `scrapy crawl LOL-Hero-Name` | 获取英雄名称，返回 JSON |
| LOLItemNameSpider | `scrapy crawl LOL-Item-Name` | 获取物品名称，返回 JSON |
| LOLItemPicSpider | `scrapy crawl LOL-Item-Pic` | 获取物品图片，下载 JPG 文件 |
| LOLHeroAvatarSpider | `scrapy crawl LOL-Hero-Avatar` | 获取英雄头像，下载 JPG 文件 |
| LOLHeroSkinSpider | `scrapy crawl LOL-Hero-Skin` | 获取英雄皮肤，下载 JPG 文件 |
| LOLHeroStorySpider | `scrapy crawl LOL-Hero-Story` | 获取英雄背景故事，返回 JSON |

## 🔧 技术栈

- **Python 3.8+**
- **Scrapy** - 强大的爬虫框架
- **Scrapy-Splash** - JavaScript 渲染支持
- **Requests** - HTTP 请求库
- **BeautifulSoup4** - HTML 解析
- **Pillow** - 图片处理
- **lxml** - 高性能 XML/HTML 解析

## ⚠️ 注意事项

1. **遵守 robots.txt**：请尊重目标网站的爬虫协议
2. **合理控制频率**：避免对服务器造成过大压力
3. **仅供学习使用**：本项目仅用于学习爬虫技术，请勿用于商业用途
4. **网站结构变化**：由于本项目创建于 2018 年，目标网站结构可能已发生变化，部分爬虫可能需要更新

## 📝 开发历史

- **2018-04** - 项目创建，完成 v1.0 版本
- **2018-04** - 引入 Scrapy 框架，完成 v2.0 版本
- **2018-04** - 开始 refactoring 分支重构工作
- **2021-08** - 更新依赖，修复安全漏洞

## 📄 License

本项目仅供学习交流使用。

---

> 🎮 *"欢迎来到英雄联盟！"* - Summoner's Rift