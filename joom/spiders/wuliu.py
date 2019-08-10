# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re


class WuliuSpider(scrapy.Spider):
    name = 'wuliu'
    allowed_domains = ['joom.com']
    # start_urls = ['http://api-merchant.joom.com/api/v3/orders/tracking?id=0O502EE3/']

    def start_requests(self):

        url = "https://api-merchant.joom.com/api/v3/orders/tracking?id="

        headers = {
            # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
            # "Content-Type": "application/json;charset=utf-8",
            # "Host": "www.joom.com",
            # "Accept-Encoding": "gzip",
            "Authorization": "Bearer SEV0001MTU2NDYyNDY2NHxad0Y5R21IRXA5b05ZRDJ4WDBRSUJnVXZZekRaeTNTcFBHWGtpclRDbGlJUUdsWXBKR1ZsMGJiZHhMV200MU5CNEpoMXFGR2VwVUp0bVliUEZSZDh4ZmVoOWZIckpPU1FKcDBXWWlxNjA5dmxfbDZER1dqM2ROaVV5SGpkdXRxSUhGWElzQkUzWW96bkN5LTRSUEdKODJnV3JraV9KS3NxSjFtNDRwc2ctOWRSTWNqYVlZQzF0ak9WV0o0bFBoVjZxX24yS0lBc1I4ZDlmTFBSQUZYQXzdAUMh7tF91g_u_2iK6eq5QlXqtRKfsx8Z47DqiMD_jA==",
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

        # SQL 查询没有物流信息语句
        sql = "SELECT wuliu.order_id \
                FROM wuliu \
	                INNER JOIN `order` ON wuliu.order_id = `order`.order_id \
	                INNER JOIN store ON `order`.store_id = store.store_id \
                WHERE \
	            wuliu.tracking_true = 'false' And `order`.order_status != 'refunded'"

        # SQL 查询5美金以上的语句

        # sql = "SELECT wuliu.order_id AS '订单号' \
        #         FROM `order` LEFT JOIN wuliu ON wuliu.order_id = `order`.order_id \
        #         WHERE wuliu.depth < 50 AND `order`.product_unitPrice * `order`.product_quantity >= 5 "


        # sql = "SELECT order_id \
        #         FROM wuliu1 "
        i=0
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                i = i+1
                print(i)
                fname = row[0]
                # 链接字符串
                # print(url + fname)
                yield scrapy.Request(url=url + fname, headers=headers, callback=self.parse)

        except:
            print('Error: unable to fecth data11')

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

        # print(response.text)

        jre = json.loads(response.text)
        # 如果有结果返回的类型是list 否则 为false
        order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))
        tracking_true = 'ture' if type(jsonpath.jsonpath(jre, '$..checkpoints[0].depth')) == list else 'false'
        # tracking_ture = type(jsonpath.jsonpath(re,'$..checkpoints[0].depth'))
        depth = jsonpath.jsonpath(jre, '$..checkpoints[-1:].depth')[0] if tracking_true == 'ture' else 'false'
        delivered = jre['data']['delivered']
        tracking_id = str(jre['data']['id'])
        trackingNumber = str(jre['data']['trackingNumber'])
        arrived = jre['data']['arrived']
        passedCustoms = jre['data']['passedCustoms']

        print(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)



        # SQL 插入语句
        # sql = "INSERT INTO wuliu1(order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms) \
        #        VALUES ('%s','%s',%s,'%s','%s','%s','%s','%s')" % \
        #       (order_id, tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms)
        # SQL 更新语句
        sql = "UPDATE wuliu SET tracking_true = '%s',delivered = '%s',depth = '%s',tracking_id = '%s',trackingNumber = '%s',arrived = '%s',passedCustoms = '%s' WHERE order_id = '%s'" % \
              (tracking_true,delivered,depth,tracking_id,trackingNumber,arrived,passedCustoms,order_id)
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






