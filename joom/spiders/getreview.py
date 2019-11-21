# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
from scrapy.selector import Selector


class GetreviewSpider(scrapy.Spider):
    name = 'getreview'
    allowed_domains = ['joom']
    start_urls = ['http://joom/']

    def start_requests(self):

        # url = "https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=0&limit=100"
        url_list = ['https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=0&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=100&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=200&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=300&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=400&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=500&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=600&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=700&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=800&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=900&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1000&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1100&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1200&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1300&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1400&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1500&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1600&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1700&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1800&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=1900&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2000&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2100&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2200&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2300&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2400&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2500&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2600&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2700&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2800&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=2900&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=3000&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=3100&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=3200&limit=100',
                    'https://api-merchant.joom.com/api/v3/reviews/multi?orderBy=orderTimestamp&order=desc&offset=3300&limit=100'
                    ]
        headers = {
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
            # "Content-Type": "application/json;charset=utf-8",
            # "Host": "www.joom.com",
            # "Accept-Encoding": "gzip",
            "Authorization": self.settings.get('JOOM_AUTH')
        }

        for url in url_list:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)


    def parse(self, response):
        # print(response.text)
        # 打开数据库连接
        db = pymysql.Connect(
            host='192.168.1.22',
            port=7306,
            user='root',
            passwd='123456',
            db='joom',
            charset='utf8'
        )

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 获取json数据
        order_list = json.loads(response.text)
        # print(order_list['data']['items'])
        # 循环导出数据
        i = 0
        for order_re in order_list['data']['items']:
            order_id = order_re['orderId']
            product_id = order_re['productId']
            categoryname = order_re['categoryName']
            order_time = re.sub(r'Z', "", re.sub(r'T', " ", order_re['orderTimestamp']))
            review_time = re.sub(r'Z', "", re.sub(r'T', " ", order_re['reviewTimestamp']))
            review_stars = order_re['starRating']
            # review_text = order_re['text']
            if jsonpath.jsonpath(order_re, '$..text') != False:
                review_text = order_re['text']
            else:
                review_text = ""
                # print(order_id)
            # print(order_time)
            # SQL 插入语句
            sql = "INSERT INTO reviews (order_id, product_id, category_name, order_time, review_time, review_stars, review_text) \
                                                       VALUES ('%s','%s','%s','%s','%s','%s','%s')" % \
                  (order_id, product_id, categoryname, order_time, review_time, review_stars, review_text)
            # print(sql)
            try:
                i = i + 1
                # 执行sql语句
                cursor.execute(sql)
                # 执行sql语句
                db.commit()
                # print(i)
                # print(sql)
            except:
                # 发生错误时回滚
                db.rollback()
                # print(222)

        # 关闭数据库连接
        db.close()
        print('采集结束')














