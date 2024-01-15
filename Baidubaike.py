# import requests
# from lxml import etree

# url = "https://baike.baidu.com/item/%E7%B3%96%E5%B0%BF%E7%97%85/100969?fromModule=lemma_search-box"

# # 发送HTTP GET请求获取页面内容
# response = requests.get(url)
# html = response.text

# # 使用lxml库解析HTML
# select = etree.HTML(html)

# # 使用XPath提取相关信息
# reference = select.xpath("//ul[@class='reference-list']/li/span[@class='link-text spec-text']/text()")[0]

# # 打印提取的信息
# print("参考资料：", reference)

import requests
from lxml import etree
import json
import sys
import time

class Spider:
    def __init__(self):
        self.UserAgent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        self.data = []

    def main(self):
        start_time = time.time()  # 记录开始时间
        index_url = "https://baike.baidu.com/wikitag/taglist?tagId=76613"
        post_url = "https://baike.baidu.com/wikitag/api/getlemmas"
        params = {
            "limit": 24,
            "timeout": 3000,
            "tagId": 76613,
            "fromLemma": False,
            "contentLength": 40,
            "page": 0
        }
        res = requests.post(post_url, params, headers=self.UserAgent)
        jsonObj = res.json()
        totalpage = jsonObj['totalPage']
        print("=======================\n总页面有" + str(totalpage) + "\n=======================\n")
        hope = int(input('请输入要下载多少页：'))
        page = 0
        while page <= hope:
            self.list_url(page)
            print('当前页面：' + str(page) + '已下载完毕')
            page = page + 1
            print('正在下载' + str(page))
        
        # Save collected data to JSON file
        self.save_to_json()

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算经过的时间
        print("爬取所有词条所需时间：", elapsed_time, "秒")

    def list_url(self, page):
        post_url = "https://baike.baidu.com/wikitag/api/getlemmas"
        params = {
            "limit": 24,
            "timeout": 3000,
            "tagId": 76625,
            "fromLemma": False,
            "contentLength": 40,
            "page": page
        }
        res = requests.post(post_url, params, headers=self.UserAgent)
        jsonObj = res.json()
        lemmaList = jsonObj['lemmaList']
        for key in lemmaList:
            self.baike(key['lemmaUrl'], key['lemmaTitle'])

    def baike(self, url, key):
        res = requests.get(url, headers=self.UserAgent)
        res.encoding = "UTF-8"
        select = etree.HTML(res.text)

        content = select.xpath("//div[@class='para MARK_MODULE']/text() | //h2[@class='title-text']/text()")   #//div[@class='para-title level-2  J-chapter ']
        content = ''.join(content)
        reference = select.xpath("//sapn[@class='link-text spec-text']/text()")
        reference = ''.join(reference).replace('\n', '')

        self.data.append({"key": key,  "content":content, "reference":reference})

        print("=======================\n" + key + "++采集并输出完毕" + "\n=======================\n")

    def save_to_json(self):
        with open("baaidubaike1.json", "w", encoding="utf-8") as f:
            for entry in self.data:
                json_entry = json.dumps(entry, ensure_ascii=False)
                f.write(json_entry + "\n")

if __name__ == '__main__':
    spider = Spider()
    spider.main()



