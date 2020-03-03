# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
from ..settings import JOOM_AUTH


class UpdaterefundSpider(scrapy.Spider):
    name = 'updaterefund'
    # allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']
    # handle_httpstatus_list = [301,302,204,206,404,500]

    # 设置不同的管道
    custom_settings = {
        'ITEM_PIPELINES': {'joom.pipelines.UpdaterefundPipeline': 301},
    }

    def start_requests(self):

        url2 = "https://api-merchant.joom.com/api/v3/orders?id="

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-Language": "zh-CN,zh;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "authorization": JOOM_AUTH
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
        # sql = "SELECT order_id.order_id FROM order_id LEFT JOIN jorder ON order_id.order_id = jorder.order_id WHERE jorder.order_id IS NULL"
        # sql = "SELECT order_id FROM order_id WHERE order_id.order_id = 'L0M544XW'"
        sql = "SELECT order_id FROM refund"
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
                yield scrapy.Request(url=url2 + order_id, headers=headers, callback=self.parse)
        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()

    def parse(self, response):

        # 获取订单数据
        product_re = json.loads(response.text)['data']
        # 处理数据
        order = {}
        # 订单id
        order['order_id'] = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))
        # 订单状态
        order['order_status'] = product_re['status']
        # 订单退款时间
        order['refund_timestamp'] = re.sub(r'Z', "", re.sub(r'T', " ", product_re['refund']['timestamp']))
        # 订单退款原因
        order['refund_reason'] = product_re['refund']['reason']
        # 订单退款方
        order['refund_by'] = product_re['refund']['by']
        # 订单退款金额
        order['refund_cost'] = product_re['refund']['cost']
        # 订单退款原始金额
        order['refund_price'] = product_re['refund']['price']
        # 订单不知道
        order['refund_fraction'] = product_re['refund']['fraction']

        yield order
