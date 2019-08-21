# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import traceback
import logging
from insurance_comment.middlewares import UrlFilterAndAdd, URLRedisFilter

logger = logging.getLogger(__name__)


class InsuranceCommentPipeline(object):
    commit_sql_str = """insert into kaixinbao(name,url,stars,useful,comments) values ("{name}","{url}","{stars}","{useful}","{comments}");"""

    commit_sql_str_huize = """insert into huize2(name,url,stars,comments) values ("{name}","{url}","{stars}","{comments}");"""

    def __init__(self, settings):
        self.dupefilter = UrlFilterAndAdd()
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):

        # self.dupefilter.add_url(item['url'])

        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        try:
            sqltext = self.commit_sql_str_huize.format(
                name=pymysql.escape_string(str(item["name"])),
                url=pymysql.escape_string(str(item["url"])),
                stars=pymysql.escape_string(str(item["stars"])),
                # useful=pymysql.escape_string(str(item["useful"])),
                comments=pymysql.escape_string(str(item["comments"]))
            )
            self.cursor.execute(sqltext)
        except Exception as e:
            logger.warning(e)

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=self.settings.get("MYSQL_HOST"),
            port=self.settings.get("MYSQL_PORT"),
            db=self.settings.get("MYSQL_DBNAME"),
            user=self.settings.get("MYSQL_USER"),
            passwd=self.settings.get("MYSQL_PASSWD"),
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
