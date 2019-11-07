# -*- coding: utf-8 -*-
import scrapy
import json
import pymysql
import re


class GetorderidSpider(scrapy.Spider):
    name = 'getorderid'
    allowed_domains = ['joom.com']

    # start_urls = ['http://joom.com/']

    def start_requests(self):

        # 循环采集

        # 店铺列表
        # store_list = ['5ac428108b2c3703c514adae']
        store_list = ['5ac428108b2c3703c514adae', '5ac5d1cd1436d4032cebcb28', '5ae965d88b4513032f9af87c',
                      '5ae970fb8b2c37038e407f13', '5ae989621436d403aa653105', '5afd36028b2c3703ba59a39c',
                      '5b14e2911436d40306a42175', '5b3086d78b2c370304e523ee', '5b611c358b4513036844961f',
                      '5b8d02af8b2c3703a7482b77', '5b8d059a8b2c3703a7485572', '5b8d05cc1436d403469f053d',
                      '5bb5b64a8b451303df3928ab', '5bc5c4c01436d4039bd805c1', '5ca339c66ecda8030142cebe',
                      '5ca33b0e6ecda8030151382a', '5ca33b8d8b4513030129d2c8', '5ca33c258b451303013153b4',
                      '5cab24ea28fc710301c11225', '5cab253d28fc710301c13a6f', '5cab25be1436d40301e06482',
                      '5cb7e6b81436d40301465d88', '5cba947436b54d0301258edc', '5cc65d5528fc710301608e44',
                      '5d072e898b2c37030128c6b7', '5d0aeaa21436d40301bfd015', '5d0b39b58b45130301432c1a',
                      '5d118eb136b54d0301b8aa3f', '5d15da4d28fc71030179a64c', '5d15db9c28fc71030179e556',
                      '5d2581358b45130301d461bf', '5d2581648b2c370301de8d81', '5d2581d41436d4030152ad1e',
                      '5d25822036b54d03019c62c3', '5d25833f36b54d03019c83ea'
                      ]


        url_list = ['https://api-merchant.joom.com/api/v3/orders/multi?offset=0&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=100&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=200&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=300&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=400&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=500&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=600&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=700&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=800&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=900&limit=100&storeId=',
                    'https://api-merchant.joom.com/api/v3/orders/multi?offset=1000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1100&limit=100&storeId='
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=1900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=2900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=3900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=4900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=5900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=6900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=7900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8800&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=8900&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9000&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9100&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9200&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9300&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9400&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9500&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9600&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9700&limit=100&storeId=',
                    # 'https://api-merchant.joom.com/api/v3/orders/multi?offset=9800&limit=100&storeId=',

                    ]

        url11='https://api-merchant.joom.com/api/v3/orders/multi?offset=200&limit=100&storeId=5d25833f36b54d03019c83ea'
        # url = 'https://api-merchant.joom.com/api/v3/orders/multi?offset=200&limit=100&storeId='

        for store_id in store_list:
            for url in url_list:

                headers = {
                    # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
                    # "Content-Type": "application/json;charset=utf-8",
                    # "Host": "www.joom.com",
                    # "Accept-Encoding": "gzip",
                    "Authorization": self.settings.get('JOOM_AUTH')
                }
                # print(url + store_id)
                yield scrapy.Request(url=url + store_id, headers=headers, callback=self.parse)


    def parse(self, response):

        # ----- 打开数据库 -----
        print("2")
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
        for order_re in order_list['data']['items']:
            order_id = order_re['id']
            order_time = re.sub(r'Z', "", re.sub(r'T', " ", order_re['orderTimestamp']))
            store_id = order_re['storeId']
            # print(order_id)
            # print(order_time)
            # SQL 插入语句
            sql = "INSERT INTO order_id (order_id, order_time, store_id) \
                                               VALUES ('%s','%s','%s')" % \
                  (order_id, order_time, store_id)
            # print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 执行sql语句
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()

        # 关闭数据库连接
        db.close()
        print('采集结束')


        # print(order_list['data']['items'][0]['id'])
        # # 如果有结果返回的类型是list 否则 为false
        # order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))
        # tracking_true = 'ture' if type(jsonpath.jsonpath(jre, '$..checkpoints[0].depth')) == list else 'false'
        # # tracking_ture = type(jsonpath.jsonpath(re,'$..checkpoints[0].depth'))
        # depth = jsonpath.jsonpath(jre, '$..checkpoints[-1:].depth')[0] if tracking_true == 'ture' else 'false'
        # delivered = jre['data']['delivered']
        # tracking_id = str(jre['data']['id'])
        # trackingNumber = str(jre['data']['trackingNumber'])
        # arrived = jre['data']['arrived']
        # passedCustoms = jre['data']['passedCustoms']

        # print(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)
