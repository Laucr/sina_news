# -*- coding: utf-8 -*-
# __author__ = "Lau"

import sys
import scrapy
import execjs

sys.path.append('..')

reload(sys)
sys.setdefaultencoding('utf8')


class SinaNewsSpider(scrapy.spiders.Spider):
    def __init__(self, name=None, **kwargs):
        super(SinaNewsSpider, self).__init__(name, **kwargs)

    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = [
        'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0'
        '&offset_num=0&num=5&asc=&r=0.9433961449038644&page='
    ]

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 '
        '(KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    ]

    # OVERRIDE
    def start_requests(self):

        for a_url in self.start_urls:
            # pages = range(1, 2)
            # for page in pages:
            yield scrapy.Request(url=(a_url + str(1)),
                                 headers={
                                     # "User-Agent": self.user_agents[random.randint(0, len(self.user_agents) - 1)]}
                                     "User-Agent": self.user_agents[0]}
                                 )

    # OVERRIDE
    def parse(self, response):
        item_counter = 5
        json_data = response.body[14:-1].decode('gbk')
        news_info = execjs.eval(json_data)
        # I love this line XD
        _items = [{
                      'title': news_info['list'][_iter]['title'].encode('utf8'),
                      'category': news_info['list'][_iter]['channel']['title'].encode('utf8'),
                      'href': news_info['list'][_iter]['url']
                  } for _iter in range(item_counter)]

        for _a_item in _items:
            yield scrapy.http.Request(url=_a_item['href'],
                                      meta={'title': _a_item['title'],
                                            'category': _a_item['category'],
                                            'href': _a_item['href']},
                                      callback=self.parse_secondary_link)

    def parse_secondary_link(self, response):
        sel = scrapy.Selector(response)
        item = {
            'title': response.meta['title'],
            'article': sel.xpath('//*[@id="artibody"]/p/text()').extract(),
            'href': response.meta['href'],
            'category': response.meta['category']
        }
        yield item
