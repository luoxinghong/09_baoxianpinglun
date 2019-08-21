# -*- coding: utf-8 -*-
from scrapy import cmdline

# cmdline.execute("scrapy crawl kaixinbao -s JOBDIR=./jobdir".split())
# cmdline.execute("scrapy crawl kaixinbao -o movie1.csv -t csv".split())
# cmdline.execute("scrapy crawl kaixinbao2".split())
cmdline.execute("scrapy crawl huize".split())
