# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re


class GetnoshippingSpider(scrapy.Spider):
    name = 'updatedeliver'
    allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']

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
        sql = "SELECT shipping.order_id FROM jorder LEFT JOIN shipping ON shipping.order_id = jorder.order_id WHERE shipping.depth < 50 AND jorder.product_unitPrice * jorder.product_quantity >= 5 AND jorder.note = 1 AND jorder.order_status != 'refunded'"
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
                # print(url + fname)
                yield scrapy.Request(url=url + order_id, headers=headers, callback=self.parse)

        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()


    def parse(self, response):

        # print(response.request.url)

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

        # print(response.text)

        shipping_re = json.loads(response.text)
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
        # sql = "INSERT INTO shipping(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms) \
        #        VALUES ('%s',%s,%s,'%s','%s','%s',%s,%s)" % \
        #       (order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)
        # SQL 更新语句
        sql = "UPDATE shipping SET tracking_true = %s,delivered = %s,depth = '%s',tracking_id = '%s',trackingNumber = '%s',arrived = %s,passedCustoms = %s WHERE order_id = '%s'" % \
              (tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms, order_id)
        # print(sql)
        try:
            print(order_id + "妥投信息已更新")
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

