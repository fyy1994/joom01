# -*- coding: utf-8 -*-
import scrapy


class EarSpider(scrapy.Spider):
    name = 'ear'
    allowed_domains = ['joom.com/en/search/q.bluetooth%20earphones']
    start_urls = ['http://joom.com/en/search/q.bluetooth%20earphones/']

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "www.joom.com",
        "Accept-Encoding": "gzip",
    }




    def parse(self, response):
        a = response.body
        print(a)
