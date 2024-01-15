# llm_crawler

# 👋Introduction

Web scraper is a Python-based tool designed to extract data from web pages and APIs. With its powerful data extraction capabilities, our scraper can automate the collection of large amounts of data from various sources, including e-commerce sites, social media platforms, and news outlets.

In this project, we use two web crawlers to scrape high-quality Chinese articles (including Simplified and Traditional Chinese) for training Chinese large language models (LLMs) in general.

## **Installation**

```
pip install -r requirements.txt
```
# 🚌**Usage**
## **Requests**
### **01 Working principle**
Coding process of requests module:
- Specify url
    - UA camouflage
    - Processing of request parameters
- Initiate a request
- Get response data
- Persistent storage

![Alt text](image-20210803105808636.png)


### **02 Examples**
#### Daily news web page（http://mrxwlb.com/category/mrxwlb-text/）
**Input**
```python
import requests
from lxml import etree
import json

urls = [f'http://mrxwlb.com/category/mrxwlb-text/page/{i}/' for i in range(1,3)]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
data = []
for url in urls:
    resp = requests.get(url=url, headers=headers)
    html = etree.HTML(resp.text)
    list = html.xpath('//header[@class="entry-header"]/h1')
    for a in list:
        title = a.xpath('./a/text()')[0].strip()
        page_url = a.xpath('./a/@href')[0]
        page_resp = requests.get(url=page_url, headers=headers)
        page_html = etree.HTML(page_resp.text)
        page_list = page_html.xpath('//section[@class="entry-content"]/p')
        text = ''
        for p in page_list:
            if p.text is not None:
                text += p.text
        data.append({"title": title, "text": text})

with open("data.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```
**Output**
```
[
  {
    "title": "2023年07月03日新闻联播文字版",
    "text": "7月3日，中共中央总书记、国家主席习..."
  },
  {
    "title": "2023年07月02日新闻联播文字版",
    "text": "在全面贯彻党的二十大精神的开局之年，我们迎来中国共产党成立102周年华诞。历史见证壮阔的行进..."
  },
  {
    "title": "2023年07月01日新闻联播文字版",
    "text": "中共中央政治局6月30日下午..."
  },
  {
    "title": "2023年06月30日新闻联播文字版",
    "text": "中共中央政治局..."
  },
  ...
]
```

## **Scrapy**
Scrapy remains by far the most popular crawler framework. Here is a part of official introduction to scrapy.

```
An open source and collaborative framework for extracting the data you need from websites.

In a fast, simple, yet extensible way.
```

The features of scrapy are: high speed, simplicity and scalability.

Scrapy official documentation: https://docs.scrapy.org/en/latest/

### **01 Working principle**

![Alt text](image-20210803111853028.png)


The whole work flow:

1. The url starting in the crawler is constructed as a request object and passed to the scheduler.

2. The `engine` gets the request object from the `scheduler`. Then give it to the `downloader`.

3. The source code of the page is obtained by the `downloader` and packaged into a response object. And feed back to the `engine`.

4. The `engine` passes the response object to the `spider`, which parses the data (parse). And feed back to the `engine`.

5. `Engine` will pass data to pipeline for data persistence or further data processing.

6. During this period, if the spider is not extracting data. Instead, the subpage url. Can be further submitted to the scheduler to repeat the process of `Step 2`


### **02 Examples**

#### 01--xianfa（宪法）
1. Start a scrapy project.
    ```
    scrapy startproject xianfa
    ```
2. Download the uploaded Xianfa.py file in the `path\xianfa\xianfa\spiders` folder or create the Xianfa.py file and copy and paste the following code into it.

3. Transfer path to `path\xianfa\xianfa\spiders`.
    ```
    d:> cd d:\path\xianfa\xianfa\spiders

    d:\path\xianfa\xianfa\spiders> scrapy crawl xianfa -o xianfa.json
    # OR
    d:\path\xianfa\xianfa\spiders> scrapy runspider xianfa.py -o xianfa.json
    ```

4. Crawled content will be saved to the `path\xianfa\xianfa\spiders` directory in json format.

- **Note:** The chapter3 web page is special and requires a second operation, that is, comment the code under "Web crawling content except chapter3", and uncomment the code under "chapter3 crawling content", and then repeat step 3 again.

**Input**
```python
import scrapy
import requests
import json

from xianlaw.items import XianlawItem


class XianfaSpider(scrapy.Spider):
    name = "xianfa"
    allowed_domains = ["www.basiclaw.gov.hk"]
    #use this when crawling others expect for chapter3
    start_urls = [f"https://www.basiclaw.gov.hk/sc/constitution/chapter{i}.html" for i in range(1,5)]

    #use this when crawling chapter3
    #start_urls = ["https://www.basiclaw.gov.hk/sc/constitution/chapter3.html"]

    def parse(self, response):
        #use this when crawling others expect for chapter3
        elements = response.xpath('//body/*')

        #use this when crawling chapter3
        #elements = response.xpath('//div[@class="list_content"]/*')

        text = ''
        title = ''
        for e in elements:
            if e.xpath('self::h2'):
                if text:
                    yield {"text": title + "：" + text}
                    text = ''
                title = e.xpath('string()').get().strip()
            elif e.xpath('self::p'):
                text += e.xpath('string()').get().strip()
                text = text.replace('\r', '').replace('\n', '')
        if text:
            yield {"text": title +"：" + text}

    def parse_start_url(self, response):
        # odering
        yield from sorted(super().parse_start_url(response), key=lambda x: int(x["text"].split(".")[0]))    
```
**Output**
```
[
	{"text": "序言:中国是世界上历史最悠久的国家之一..."},
	{"text": "第一条：中华人民共和国是工人阶级领导的..."},
	{"text": "第二条：中华人民共和国的一切权力属于人民。..."},
	...
	{"text": "第一百四十三条：中华人民共和国首都是北京。"}
]

```

### **02--basiclaw（基本法）**

1. Start a scrapy project.
```
scrapy startproject basiclaw
```
2. Download the uploaded basiclaw.py file in the `path\basiclaw\basiclaw\spiders` folder or create a basiclaw.py file and copy and paste the following code into it.

3. Transfer path to `path\basiclaw\basiclaw\spiders `.
```
d:> cd d:\path\basiclaw\basiclaw\spiders

d:\path\basiclaw\basiclaw\spiders> scrapy crawl basiclaw -o basiclaw.json
#OR
d:\path\basiclaw\basiclaw\spiders> scrapy runspider basiclaw.py -o basiclaw.json
```

4. Crawling content is saved as json to the `path\basiclaw\basiclaw\spiders`.
- **Note:** The chapter4,5 page is special and requires a second operation, that is, comment the code that has been marked "Web crawling content except chapter4,5", and uncomment the code that has been marked "chapter4,5 crawling content", and repeat step 3 again

Here is the code.
```python
import scrapy
from xianlaw.items import XianlawItem
import re

class XianfaSpider(scrapy.Spider):
    name = "basiclaw"
    allowed_domains = ["www.basiclaw.gov.hk"]
    url_list = [
        "https://www.basiclaw.gov.hk/sc/basiclaw/decree.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/basiclaw.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/preamble.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter1.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter2.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter3.html",
                # "https://www.basiclaw.gov.hk/sc/basiclaw/chapter4.html",
                # "https://www.basiclaw.gov.hk/sc/basiclaw/chapter5.html"
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter6.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter7.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter8.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/chapter9.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/annex-instrument.html",
                "https://www.basiclaw.gov.hk/sc/basiclaw/national-laws.html"
                ]
    def start_requests(self):
        for url in self.url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #use this when crawling other chapters except for chapter4 and 4
        elements = response.xpath('//body/*')
        #use this when crawling chapter4 and 5
        #elements = response.xpath('//div[@class="list_content"]/*')

        text = ''
        title = ''
        for e in elements:
            if e.xpath('self::h2'):
                if text:
                    yield {"text": title + "：" + text}
                    text = ''
                title = e.xpath('string()').get().strip()
            elif e.xpath('self::p'):
                text += e.xpath('string()').get().strip()
                text = text.replace('\r', '').replace('\n', '')
        if text:
            yield {"text": title +"：" + text}

    def parse_start_url(self, response):
        # Odering
        yield from sorted(super().parse_start_url(response), key=lambda x: int(x["text"].split(".")[0]))    
```
**Output**
```
[
	{"text": "中华人民共和国主席令：第二十六号《中华人民共和国香港特别行政区基本法》..."},
	{"text": "中华人民共和国香港特别行政区基本法：..."},
	{"text": "序言：香港自古以来就是中国的领土..."},
	...
	{"text": "第一百五十九条：本法的修改权属于全国人民代表大会。..."},
	{"text": "第一百六十条：香港特别行政区成立时，香港原有..."}
]
```
---
## scrapy基础教程

​	接下来, 我们用scrapy来完成一个超级简单的爬虫, 目标: 深入理解Scrapy工作的流程, 以及各个模块之间是如何搭配工作的. 

1. 创建项目

    ```
    scrapy startproject 项目名称
    ```

    示例:

    ```
    scrapy startproject mySpider_2
    ```

    创建好项目后, 我们可以在pycharm里观察到scrapy帮我们创建了一个文件夹, 里面的目录结构如下:

    ```python
    mySpider_2   # 项目所在文件夹, 建议用pycharm打开该文件夹
        ├── mySpider_2  		# 项目跟目录
        │   ├── __init__.py
        │   ├── items.py  		# 封装数据的格式
        │   ├── middlewares.py  # 所有中间件
        │   ├── pipelines.py	# 所有的管道
        │   ├── settings.py		# 爬虫配置信息
        │   └── spiders			# 爬虫文件夹, 稍后里面会写入爬虫代码
        │       └── __init__.py
        └── scrapy.cfg			# scrapy项目配置信息,不要删它,别动它,善待它. 
    
    ```

2. 创建爬虫

    ```python
    cd 文件夹  # 进入项目所在文件夹
    scrapy genspider 爬虫名称 允许抓取的域名范围
    ```

    示例:

    ```
    cd mySpider_2
    scrapy genspider youxi 4399.com
    ```

    效果:

    ```python
    (base) sylardeMBP:第七章 sylar$ cd mySpider_2
    (base) sylardeMBP:mySpider_2 sylar$ ls
    mySpider_2      scrapy.cfg
    (base) sylardeMBP:mySpider_2 sylar$ scrapy genspider youxi http://www.4399.com/
    Created spider 'youxi' using template 'basic' in module:
      mySpider_2.spiders.youxi
    (base) sylardeMBP:mySpider_2 sylar$ 
    ```

    至此, 爬虫创建完毕, 我们打开文件夹看一下. 

    ```python
    ├── mySpider_2
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       └── youxi.py   # 多了一个这个. 
    └── scrapy.cfg
    
    ```

    

3. 编写数据解析过程

    完善youxi.py中的内容. 

    ```python
    import scrapy
    
    class YouxiSpider(scrapy.Spider):
        name = 'youxi'  # 该名字非常关键, 我们在启动该爬虫的时候需要这个名字
        allowed_domains = ['4399.com']  # 爬虫抓取的域.
        start_urls = ['http://www.4399.com/flash/']  # 起始页
    
        def parse(self, response, **kwargs):
            # response.text  # 页面源代码
            # response.xpath()  # 通过xpath方式提取
            # response.css()  # 通过css方式提取
            # response.json() # 提取json数据
    
            # 用我们最熟悉的方式: xpath提取游戏名称, 游戏类别, 发布时间等信息
            li_list = response.xpath("//ul[@class='n-game cf']/li")
            for li in li_list:
                name = li.xpath("./a/b/text()").extract_first()
                category = li.xpath("./em/a/text()").extract_first()
                date = li.xpath("./em/text()").extract_first()
    
                dic = {
                    "name": name,
                    "category": category,
                    "date": date
                }
    
                # 将提取到的数据提交到管道内.
                # 注意, 这里只能返回 request对象, 字典, item数据, or None
                yield dic
    
    ```

    注意: 

    ==spider返回的内容只能是字典, requestes对象, item数据或者None. 其他内容一律报错==

    运行爬虫: 

    ```cmd
    scrapy crawl 爬虫名字
    ```

    实例:

    ```
    scrapy crawl youxi
    ```

    

4. 编写pipeline.对数据进行简单的保存

    数据传递到pipeline, 我们先看一下在pipeline中的样子. 

    首先修改settings.py文件中的pipeline信息

    ```python
    ITEM_PIPELINES = {
        # 前面是pipeline的类名地址               
        # 后面是优先级, 优先级月低越先执行
       'mySpider_2.pipelines.Myspider2Pipeline': 300,
    }
    ```

    然后我们修改一下pipeline中的代码:

    ```python
    class Myspider2Pipeline:
        # 这个方法的声明不能动!!! 在spider返回的数据会自动的调用这里的process_item方法. 
        # 你把它改了. 管道就断了
        def process_item(self, item, spider):
            print(item)
            return item
    ```

    

## 自定义数据传输结构item

​		在上述案例中, 我们使用字典作为数据传递的载体, 但是如果数据量非常大. 由于字典的key是随意创建的. 极易出现问题,  此时再用字典就不合适了. Scrapy中提供item作为数据格式的声明位置. 我们可以在items.py文件提前定义好该爬虫在进行数据传输时的数据格式. 然后再写代码的时候就有了数据名称的依据了. 

item.py文件

```python
import scrapy

class GameItem(scrapy.Item):
    # 定义数据结构
    name = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
```

spider中. 这样来使用:

```python
from mySpider_2.items import GameItem

# 以下代码在spider中的parse替换掉原来的字典
item = GameItem()
item["name"] = name
item["category"] = category
item["date"] = date
yield item
```



## scrapy使用小总结

至此, 我们对scrapy有了一个非常初步的了解和使用. 快速总结一下. scrapy框架的使用流程: 

1. 创建爬虫项目.   `scrapy startproject xxx     `
2. 进入项目目录.    `cd xxx  `
3. 创建爬虫            `scrapy genspider 名称 抓取域`
4. 编写`item.py` 文件, 定义好数据item
5. 修改spider中的parse方法. 对返回的响应response对象进行解析. 返回item
6. 在pipeline中对数据进行保存工作. 
7. 修改`settings.py`文件, 将pipeline设置为生效, 并设置好优先级
8. 启动爬虫   `scrapy crawl 名称`

