# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time
import datetime


class GetshippingtimeSpider(scrapy.Spider):
    name = 'getshippingtime'
    allowed_domains = ['joom.com']
    start_urls = ['http://joom.com/']

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
        sql = "SELECT shipping.order_id FROM shipping LEFT JOIN shipping_time ON shipping.order_id = shipping_time.order_id WHERE depth = 60 AND shipping_time.order_id IS NULL"
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

        shipping_re = json.loads(response.text)

        # 订单编号
        order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))

        delivered = shipping_re['data']['checkpoints']
        # 有上网信息时间
        shippingtime = jsonpath.jsonpath(shipping_re, '$..checkpoints[1].ts')[0]
        timeArray = time.localtime(shippingtime / 1000)
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # print(starttime)
        # 确认收货时间
        shippedtime = jsonpath.jsonpath(shipping_re, '$..checkpoints[-1:].ts')[0]
        timeArray2 = time.localtime(shippedtime / 1000)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
        # print(endtime)
        # 计算两个时间之间的天数
        timeday = shippedtime - shippingtime
        start_date = time.strftime("%Y-%m-%d", timeArray)
        end_date = time.strftime("%Y-%m-%d", timeArray2)
        start_sec = time.mktime(time.strptime(start_date, '%Y-%m-%d'))
        end_sec = time.mktime(time.strptime(end_date, '%Y-%m-%d'))
        work_days = int((end_sec - start_sec) / (24 * 60 * 60))
        # print(work_days)

        sql = "INSERT INTO shipping_time (order_id, shipping_day, start_time, end_time) \
                                                       VALUES ('%s','%s','%s','%s')" % \
              (order_id, work_days, starttime, endtime)

        # print(sql)
        try:
            print(sql)
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

