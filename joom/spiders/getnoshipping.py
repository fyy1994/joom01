# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re


class GetnoshippingSpider(scrapy.Spider):
    name = 'getnoshipping'
    allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']
    # handle_httpstatus_list = [404]

    def start_requests(self):

        url = "https://api-merchant.joom.com/api/v3/orders/tracking?id="

        headers = {
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
            # "Content-Type": "application/json;charset=utf-8",
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
                # 链接字符串
                # print(url + order_id)
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
        # print(2222)
        # print(response.text)

        shipping_re = json.loads(response.text)
        # print(shipping_re)
        # if shipping_re['code'] == 1000 :
        #     sql = "INSERT INTO shipping(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms) \
        #                    VALUES ('%s',%s,%s,'%s','%s','%s',%s,%s)" % \
        #           (str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0)), True, False, 10, '0', '0', False, '0')
        # else:

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
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

