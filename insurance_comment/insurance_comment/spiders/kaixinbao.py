# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from insurance_comment.items import InsuranceCommentItem
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy_splash import SplashTextResponse, SplashJsonResponse, SplashResponse
from scrapy.http import HtmlResponse
from lxml import etree


class KaixinbaoSpider(CrawlSpider):
    name = 'kaixinbao'
    allowed_domains = ['kaixinbao.com']

    cookie_str = 'loginMemberId=ec35c2f86e7542a7a63e34f8dd5e83b0; acw_tc=76b20f6015534995147826541e4a533b27a2cf1c6f20300e078d1aff3e46fa; gr_user_id=bb7af5a7-2721-4a2b-8758-3529b833eef4; NTKF_T2D_CLIENTID=guest28EAEEA1-4515-B822-D4E1-B3C996E91614; grwng_uid=a3ace9c9-9f2c-4e48-87c6-906de8e93ebc; JSESSIONID=6A9C5039B6AA2C94319A6EDF8D0A6B18; __utmc=213028622; __utmz=213028622.1553499932.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_2d7e032a5f8d4e609feb9e22c0cb83f8=1553499933; _pk_ref.1.267b=%5B%22title%22%2C%22kxb%22%2C1553502407%2C%22https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fZAwkY06Odx0Kp7N6AqbF9T000005IED-C00000Y-5s_6.THvOJVjD_pn0UWdBmy-bIy9EUyNxTAT0T1d9PAwBPyf4uW0snjK9nyF-0ZRqfbwDPHnvPHcdnjD4n1-Af1IDnRcYP1b3wjczn17anRn0mHdL5iuVmv-b5HnznjcdPjDdrj0hTZFEuA-b5HDv0ARqpZwYTjCEQLILIz4omy-3py4Bmyt8mvqVQ1qdIAdxTvqdThP-5yFsR7ChIgwVgvd-uA-dUHdffzudIAdxmv7VTA7Guv3qIA-YUARhIgwVgLw-ThYqpL9BFMNYUNqWUv4Yuy4Y5iN7PiNafzR3naN7PiNawBR3nzN7PaNawBR4waN7PaNawBR4waN7riR4riNKriN7PzNawaR4niN7PiNKwiR4raN7PzNawaR4nfKWThnqPH0kn1m%26tpl%3Dtpl_11534_19347_15370%26l%3D1511157751%26attach%3Dlocation%3D%26linkName%3D%25E6%25A0%2587%25E5%2587%2586%25E5%25A4%25B4%25E9%2583%25A8-%25E6%25A0%2587%25E9%25A2%2598-%25E4%25B8%25BB%25E6%25A0%2587%25E9%25A2%2598%26linkText%3D%25E5%25BC%2580%25E5%25BF%2583%25E4%25BF%259D%25E4%25BF%259D%25E9%2599%25A9%25E7%25BD%2591%25E5%25AE%2598%25E7%25BD%2591%26xp%3Did(%2522m3202541580_canvas%2522)%252FDIV%255B1%255D%252FDIV%255B1%255D%252FDIV%255B1%255D%252FDIV%255B1%255D%252FDIV%255B1%255D%252FH2%255B1%255D%252FA%255B1%255D%26linkType%3D%26checksum%3D199%26wd%3D%E5%BC%80%E5%BF%83%E4%BF%9D%26issp%3D1%26f%3D8%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26oq%3D%25E5%258D%2597%25E6%2598%258C%25E5%25A4%25A9%25E6%25B0%2594%26inputT%3D3714%26bs%3D%E5%8D%97%E6%98%8C%E5%A4%A9%E6%B0%94%22%5D; _pk_ses.1.267b=1; a6211e66e314d44f_gr_session_id=aad9fe76-2ed1-47be-9f60-696d529af430; a6211e66e314d44f_gr_session_id_aad9fe76-2ed1-47be-9f60-696d529af430=true; __utma=213028622.2132396862.1553499932.1553499932.1553502918.2; __utmt=1; __utmb=213028622.1.10.1553502918; Hm_lpvt_2d7e032a5f8d4e609feb9e22c0cb83f8=1553502922; vlid_1001=------gjwaQzEy18688031990---------1553443200155349959915535029222--1--0--5--0--; SESSION=7426fd3b-70ca-4412-86e8-593a07b13e45; Hm_lvt_b0d61b2de58bce03e74718744c2eb82d=1553499527,1553499562,1553502408,1553503389; _pk_id.1.267b=3b5698270dcc83c5.1553499522.2.1553503422.1553502407.; nTalk_CACHE_DATA={uid:kf_9401_ISME9754_guest28EAEEA1-4515-B8,tid:1553499526889263,opd:1}; SERVERID=94e15f4ec3d49e09af658885a9abed1b|1553503416|1553499514; Hm_lpvt_b0d61b2de58bce03e74718744c2eb82d=1553503422; nTalk_PAGE_MANAGE={|m|:[{|39924|:|034322|},{|11994|:|034322|},{|21806|:|034322|}],|t|:|16:43:52|}'

    headers = {'Host': 'www.kaixinbao.com',
               'Connection': 'keep-alive',
               'Cache-Control': 'no-cache',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Upgrade-Insecure-Requests': '1',
               'Pragma': 'no-cache',
               'Cookie': cookie_str
               }

    # start_urls = ['http://www.kaixinbao.com', 'http://www.kaixinbao.com/Search/Search.jsp?query=','http://www.kaixinbao.com/lvyou-baoxian/',
    #               'http://www.kaixinbao.com/yiwai-baoxian/',
    #               'http://www.kaixinbao.com/jiankang-baoxian/', 'http://www.kaixinbao.com/renshou-baoxian/',
    #               'http://www.kaixinbao.com/jiacai-baoxian/', 'http://www.kaixinbao.com/jiacai-baoxian/',
    #               'http://www.kaixinbao.com/tx/', 'http://www.kaixinbao.com/chexian/']
    file = open("./insurance_urls.txt", encoding="utf-8")
    start_urls = file.readlines()
    start_urls = [i.replace("\n","") for i in start_urls]

    rules = (
        Rule(LinkExtractor(allow='-baoxian/\d+.shtml'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        # print(response.body.decode())
        url = response.url
        name = etree.HTML(response.body.decode()).xpath("//title/text()")[0].replace("\n", "")
        print(name)

        item = InsuranceCommentItem()
        item["name"] = name
        item["url"] = url
        item["comments"] = ''
        yield item
        print("*" * 100)

    def splash_request(self, request):
        return SplashRequest(url=request.url, args={'wait': 10})

    # 重写CrawlSpider 的方法
    def _requests_to_follow(self, response):

        if not isinstance(response, (SplashTextResponse, SplashJsonResponse, SplashResponse, HtmlResponse)):
            return
        print('==========================进入_requests_to_follow=========================')
        seen = set()

        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _build_request(self, rule, link):
        # 重要！！！！！这里重写父类方法，特别注意，需要传递meta={'rule': rule, 'link_text': link.text}
        # 详细可以查看 CrawlSpider 的源码
        r = SplashRequest(url=link.url, callback=self._response_downloaded, meta={'rule': rule, 'link_text': link.text},
                          args={'wait': 5, 'url': link.url})
        r.meta.update(rule=rule, link_text=link.text)
        return r