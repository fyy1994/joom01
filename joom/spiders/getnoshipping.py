# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time


class GetnoshippingSpider(scrapy.Spider):
    name = 'getnoshipping'
    allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']
    handle_httpstatus_list = [404]

    def start_requests(self):

        url = "https://api-merchant.joom.com/api/v3/orders/tracking?id="

        headers = {
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-version": "0.1.0",
            # "Host": "www.joom.com",
            # "Accept-Encoding": "gzip",
            "Authorization": self.settings.get('JOOM_AUTH')
        }


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

        # SQL 查询还没有查询物流信息语句
        sql = "SELECT order_id.order_id  FROM order_id LEFT JOIN shipping ON order_id.order_id = shipping.order_id WHERE shipping.order_id IS NULL"
        i = 0
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                i = i + 1
                print(i)
                order_id = row[0]
                print(order_id)
                # 链接字符串
                yield scrapy.Request(url=url + order_id, headers=headers, callback=self.parse)

        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()

    def parse(self, response):

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

        if response.status == 404:
            order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))

            sql = "INSERT INTO shipping(order_id, tracking_true) \
                               VALUES ('%s', %s)" % \
                  (order_id, 0)

        else:

            shipping_re = json.loads(response.text)
            # print(shipping_re)
            # if shipping_re['code'] == 1000 :
            #     sql = "INSERT INTO shipping(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms) \
            #                    VALUES ('%s',%s,%s,'%s','%s','%s',%s,%s)" % \
            #           (str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0)), True, False, 10, '0', '0', False, '0')
            # else:
            # print(shipping_re)
            # 处理数据
            order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))
            # 如果有结果返回的类型是list 否则 为false
            tracking_true = 'True' if type(jsonpath.jsonpath(shipping_re, '$..checkpoints[0].depth')) == list else 'False'
            # tracking_ture = type(jsonpath.jsonpath(re,'$..checkpoints[0].depth'))
            depth = jsonpath.jsonpath(shipping_re, '$..checkpoints[-1:].depth')[0] if tracking_true == 'True' else 'False'
            delivered = shipping_re['data']['delivered']
            tracking_id = str(shipping_re['data']['id'])
            trackingNumber = str(shipping_re['data']['trackingNumber'])
            arrived = shipping_re['data']['arrived']
            passedCustoms = shipping_re['data']['passedCustoms']

            # print(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)

            # SQL 插入语句
            sql = "INSERT INTO shipping(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms) \
                   VALUES ('%s',%s,%s,'%s','%s','%s',%s,%s)" % \
                  (order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)

        # print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            print(order_id + "订单物流信息已插入")
        except pymysql.Error as e:
            # 发生错误时回滚
            print("错误代码 %d: %s" % (e.args[0], e.args[1]))
            # print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            print(sql)
            db.rollback()
            print(order_id + "出现错误")

        # 关闭数据库连接
        db.close()

