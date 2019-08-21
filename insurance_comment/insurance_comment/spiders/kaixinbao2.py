# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from insurance_comment.items import InsuranceCommentItem
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
from lxml import etree
from scrapy import Request


class Kaixinbao2Spider(scrapy.Spider):
    name = 'kaixinbao2'
    allowed_domains = ['kaixinbao.com']

    file = open("./insurance_urls.txt", encoding="utf-8")
    start_urls = file.readlines()
    start_urls = [i.replace("\n", "") for i in start_urls]


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        url = response.url
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="chromedriver",chrome_options=chrome_options)
        driver.get(url)
        time.sleep(5)
        comment_button = driver.find_element_by_id("count").click()
        time.sleep(10)

        stars = re.findall('<span class="as_stars_(.*?)">', driver.page_source)
        useful = re.findall('title="有用" count="(.*?)"', driver.page_source)
        contents = re.findall('class="icon_p"></span>(.*?)</', driver.page_source)

        total = re.findall('用户评价<span>[(](.*?)[)]</span>', driver.page_source)[0]
        name = etree.HTML(driver.page_source).xpath("//title/text()")[0].replace("\n", "")
        # print("1",stars)
        # print("1",useful)
        # print("1",contents)
        print(url)
        print("name",name)
        print("total",total)

        if int(total) > 10:
            for i in range(int(total) // 10 ):
                page = driver.find_element_by_partial_link_text(u'下一页')
                driver.execute_script("arguments[0].scrollIntoView(false);",page)
                next_comment_button = driver.find_element_by_xpath("//li[@class='page_next']/a[1]").click()
                time.sleep(5)
                stars_temp = re.findall('<span class="as_stars_(.*?)">', driver.page_source)
                useful_temp = re.findall('title="有用" count="(.*?)"', driver.page_source)
                contents_temp = re.findall('class="icon_p"></span>(.*?)</', driver.page_source)
                print(stars_temp)
                print(useful_temp)
                print(contents_temp)
                stars.extend(stars_temp)
                useful.extend(useful_temp)
                contents.extend(contents_temp)


        driver.close()
        item = InsuranceCommentItem()
        item["name"] = name
        item["url"] = url
        item["stars"] = stars
        item["useful"] = useful
        item["comments"] = contents
        yield item
        print("*" * 100)






