# -*- coding: utf-8 -*-
# __author__ = "Lau"

import random
import sys
import urllib

import scrapy

sys.path.append('..')

reload(sys)
sys.setdefaultencoding('utf8')


class SinaNewsSpider(scrapy.spiders.Spider):
    def __init__(self, name=None, **kwargs):
        super(SinaNewsSpider, self).__init__(name, **kwargs)

    name = 'sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = [
        'http://roll.news.sina.com.cn/s/'
        'channel.php?ch=01#col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=80&asc=&page=',
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
            pages = range(1, 200)
            for page in pages:
                yield scrapy.Request(url=(a_url + str(page)),
                                     headers={
                                         "User-Agent": self.user_agents[random.randint(0, len(self.user_agents) - 1)]})

    # OVERRIDE
    def parse(self, response):
        item_size = 80
        # I love this line XD
        _items = [
            {
                'title': [a_title.extract() for a_title in response.xpath('//div[@class="info"]/h2/a/@title')][_iter],
                '_id': [a_id.extract() for a_id in response.xpath('//div[@class="info"]/h2/a/@href')][_iter]
            } for _iter in range(item_size)
            ]

        for _a_item in _items:
            yield scrapy.http.Request(url=_a_item['_id'].encode('utf8'),
                                      headers={
                                          "User-Agent": self.user_agents[random.randint(0, len(self.user_agents) - 1)]},
                                      meta={'title': _a_item['title'].encode('utf8'),
                                            'category': urllib.unquote(response.url.split('/')[-1].split('?')[0])},
                                      callback=self.parse_secondary_link)

    def parse_secondary_link(self, response):
        sel = scrapy.Selector(response)
        item = {
            'title': response.meta['title'],
            'article': sel.xpath('//*[@id="artibody"]/p[1]/text()').extract()[0].encode('utf8'),
            'category': response.meta['category']
        }
        yield item
