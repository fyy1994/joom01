# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
from ..settings import JOOM_AUTH


class GetorderSpider(scrapy.Spider):
    name = 'getorder'
    # allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']
    # handle_httpstatus_list = [301,302,204,206,404,500]

    # 设置不同的管道
    custom_settings = {
        'ITEM_PIPELINES': {'joom.pipelines.GetorderPipeline': 301},
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
        sql = "SELECT order_id.order_id FROM order_id LEFT JOIN jorder ON order_id.order_id = jorder.order_id WHERE jorder.order_id IS NULL"
        # sql = "SELECT order_id FROM order_id WHERE order_id.order_id = 'L0M544XW'"
        # sql = "SELECT order_id FROM wuliu1"
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
        # 订单创建时间
        order['order_time'] = re.sub(r'Z', "", re.sub(r'T', " ", product_re['orderTimestamp']))
        # 订单上次更新时间
        order['update_timestamp'] = re.sub(r'Z', "", re.sub(r'T', " ", product_re['updateTimestamp']))
        # 订单状态
        order['order_status'] = product_re['status']
        # 店铺id
        order['store_id'] = product_re['storeId']
        # 商品id
        order['product_id'] = product_re['product']['id']
        # 流水id
        order['transaction_id'] = product_re['transactionId']
        # 不知道什么的id
        order['customer_id'] = product_re['customerId']
        # 商品sku
        order['product_sku'] = product_re['product']['variant']['sku']
        # 商品单价
        order['product_unitPrice'] = jsonpath.jsonpath(product_re, '$..unitPrice')[0]
        # 商品运费单价
        order['product_shippingPrice'] = jsonpath.jsonpath(product_re, '$..shippingPrice')[0]
        # 商品数量
        order['product_quantity'] = product_re['quantity']
        # 客户国家
        order['order_country'] = product_re['shippingAddress']['country']
        # 订单什么得
        order['order_origAmount'] = jsonpath.jsonpath(product_re, '$..origAmount')[0]
        # 商品总价
        order['order_price'] = jsonpath.jsonpath(product_re, '$..orderPrice')[0]
        # 商品佣金价格
        order['order_cost'] = jsonpath.jsonpath(product_re, '$..orderCost')[0]
        # 商品一些标记信息
        order['specialLogisticsPriceConditions'] = jsonpath.jsonpath(product_re, '$..specialLogisticsPriceConditions')[0]
        # 运费是由谁出的
        order['joomShippingPriceUsed'] = jsonpath.jsonpath(product_re, '$..joomShippingPriceUsed')[0]
        # 运输方式
        order['shipping_Method'] = product_re['shippingMethod']

        # 如果订单有物流单号
        if jsonpath.jsonpath(product_re,'$..shipment') != False:

            # 订单运输时间
            order['shipping_timestamp'] = re.sub(r'Z', "", re.sub(r'T', " ", product_re['shipment']['timestamp']))
            # print(shipping_timestamp)
            # 运输渠道
            order['shipping_provider'] = product_re['shipment']['provider']
            # 运输id
            order['shipping_provider_id'] = product_re['shipment']['providerId']
            # 货运单号
            order['shipping_trackingNumber'] = product_re['shipment']['trackingNumber']
            # 运输的另一个运单号
            order['shipping_OrderNumber'] = jsonpath.jsonpath(product_re,'$..shippingOrderNumber')[0] if jsonpath.jsonpath(product_re,'$..shippingOrderNumber') != False else ""

        else:
            order['shipping_timestamp'] = re.sub(r'Z', "", re.sub(r'T', " ", product_re['updateTimestamp']))
            order['shipping_provider'] = ''
            order['shipping_provider_id'] = ''
            order['shipping_trackingNumber'] = ''
            order['shipping_OrderNumber'] = ''

        # 判断订单是否已经退款
        if jsonpath.jsonpath(product_re, '$..refund'):

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
