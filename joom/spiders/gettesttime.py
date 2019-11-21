# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time
from scrapy.selector import Selector


class GettesttimeSpider(scrapy.Spider):
    name = 'gettesttime'
    # allowed_domains = ['track.yw56.com.cn/zh-CN']
    # 设置爬虫速度
    # custom_settings = {'DOWNLOAD_DELAY': 0.25}
    # start_urls = ['http://track.yw56.com.cn/zh-CN']
    # handle_httpstatus_list = [301,302,204,206,404,500]

    def start_requests(self):
        # url = 'https://aamz.mabangerp.com/index.php?mod=order.getOrderLog'
        url = 'https://aamz.mabangerp.com/index.php?mod=order.findrelevantinfo'

        headers = {
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            # "Cache-Control": "no-cache",
            # "Connection": "keep-alive",
            # "Content-Type": "application/json; charset=UTF-8",

            # "Host": "aamz.mabangerp.com",
            # "Content-Length": "",
            # "X-Requested-With": "XMLHttpRequest",
            # "Referer": "https://aamz.mabangerp.com/index.php?mod=order.detail&platformOrderId=0O43LJNW&orderStatus=2&orderTable=2&tableBase=2&cMKey=MABANG_ERP_PRO_MEMBERINFO_LOGIN_191565&lang=cn",

            # 注意user-agent不要出现空格
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
        }

        data1 = {
            'orderId': '14856905',
            'type': '1',
            'tableBase': '2'
        }

        cookies = "lang=cn; signed=222014_00f6735cc675f0abb6f483d9913f72bf; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22222014%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%2271e0f1c4b322ee31a32e6079fdc2938c%22%3B%7D; CRAWL_KANDENG_KEY=K6uqW0ZkQEouz0n1adoI%2FWqfFs2PbJ8%2BCpQKvtnzAvWpTX174VXBmq5L9cDOSOj%2Bm2IcDf7pRauH34yzR4OEyw%3D%3D; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; PHPSESSID=sq9njg1nvkfpravfdfbibg0du0"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

        yield scrapy.FormRequest(url=url, cookies=cookies, formdata=data1, callback=self.parse)



    def parse(self, response):
        # 处理数据
        # shipping_re = response
        # print(shipping_re.text)

        # re = response.text
        # re_list = re.encode('utf8').decode('unicode_escape')


        re_list = json.loads(response.text)
        re = re_list['orderhtml']
        #
        # # 订单编号
        order_id_list = Selector(text=re).xpath('//a/text()').extract()
        #
        print(re)
        print(order_id_list)


