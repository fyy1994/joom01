# -*- coding: utf-8 -*-
import scrapy


class JoomproductidSpider(scrapy.Spider):
    name = 'joomProductID'
    allowed_domains = ['www.joom.com/en/search/q.bluetooth earphones']
    start_urls = ['https://www.joom.com/en/search/q.bluetooth earphones']

    def parse(self, response):
        a = response.body
        print(a)

