# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re
from scrapy import Request
import requests
from copy import deepcopy
from insurance_comment.items import InsuranceCommentItem_huize


class HuizeSpider(scrapy.Spider):
    name = 'huize'
    allowed_domains = ['huize.com']
    start_urls = ['http://huize.com/']
    prefix_url = "https://www.huize.com/product/prodreview/showlist{}-{}.html?type=0"
    # 获取全部保险的搜索页
    # prefix_url = "https://search.huize.com/p-{}-%20-0-0-1"
    # https: // search.huize.com / p - 42 - % 20 - 0 - 0 - 1

    headers = {
               'Cache-Control': 'no-cache',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Upgrade-Insecure-Requests': '1',
               'Pragma': 'no-cache',
               }

    file = open("./huize_url.txt", encoding="utf-8")
    urls = [i.replace("\n", "") for i in file.readlines()]

    def start_requests(self):
        for url in self.urls:
            product_id = re.findall("detail-(.*?).html", url)[0]
            yield Request(self.prefix_url.format(product_id, 1), callback=self.parse,meta={"product_id":product_id,"first_url":url},dont_filter=True)

    def parse(self, response):
        url = response.url
        meta = deepcopy(response.meta)
        html = response.body.decode()
        name = re.findall('"productName": "(.*?)",',html)[0]
        print(url)
        print(name)
        # print(html)
        stars = re.findall(r'"attitudeLevel": (.*?),', html)
        comments = re.findall(r'"content": "(.*?)",', html)
        total = int(re.findall('"count":(.*?),', html)[0])

        if total > 10:
            if total // 10 == 0:
                page_number = total // 10 + 1
            else:
                page_number = total // 10 + 2
            print("page_number",page_number)
            for i in range(2, page_number):
                res = requests.get(self.prefix_url.format(meta["product_id"],i),headers=self.headers).content.decode()
                stars_temp = re.findall(r'"attitudeLevel": (.*?),', res)
                comments_temp = re.findall(r'"content": "(.*?)",', res)
                stars.extend(stars_temp)
                comments.extend(comments_temp)
        item = InsuranceCommentItem_huize()
        item["name"] = name
        item["url"] = meta["first_url"]
        item["stars"] = stars
        item["comments"] = comments
        print("1stars:", len(stars))
        print("2:comments", len(comments))
        print("3total:", total)
        yield item
        print("*" * 150)
