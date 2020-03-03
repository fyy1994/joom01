# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re



class UpdatewuliuwentiSpider(scrapy.Spider):
    name = 'updatewuliuwenti'
    allowed_domains = ['joom']
    # start_urls = ['http://joom/']

    def start_requests(self):

        url = "https://api-merchant.joom.com/api/v3/orders?id="

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
        # sql = "SELECT order_id FROM jorder WHERE order_status = 'fulfilledOnline' OR order_status = 'approved' "
        sql = "SELECT 订单号 FROM view_wenti"

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

        # print(response.text)

        product_re = json.loads(response.text)['data']
        # 处理数据

        order_id = str(re.compile(r"(?<==)(.+?)\b").search(response.request.url).group(0))

        order_time = re.sub(r'Z', "", re.sub(r'T', " ", product_re['orderTimestamp']))
        update_timestamp = re.sub(r'Z', "", re.sub(r'T', " ", product_re['updateTimestamp']))
        order_status = product_re['status']
        store_id = product_re['storeId']
        product_id = product_re['product']['id']
        transaction_id = product_re['transactionId']
        customer_id = product_re['customerId']
        product_sku = product_re['product']['variant']['sku']
        product_unitPrice = jsonpath.jsonpath(product_re, '$..unitPrice')[0]
        product_shippingPrice = jsonpath.jsonpath(product_re, '$..shippingPrice')[0]
        product_quantity = product_re['quantity']
        order_country = product_re['shippingAddress']['country']
        order_origAmount = jsonpath.jsonpath(product_re, '$..origAmount')[0]
        order_price = jsonpath.jsonpath(product_re, '$..orderPrice')[0]
        order_cost = jsonpath.jsonpath(product_re, '$..orderCost')[0]
        specialLogisticsPriceConditions = jsonpath.jsonpath(product_re, '$..specialLogisticsPriceConditions')[0]
        joomShippingPriceUsed = jsonpath.jsonpath(product_re, '$..joomShippingPriceUsed')[0]
        shipping_Method = product_re['shippingMethod']
        # print(product_re['shipment']['timestamp'])
        if jsonpath.jsonpath(product_re, '$..shipment') != False:

            shipping_timestamp = re.sub(r'Z', "", re.sub(r'T', " ", product_re['shipment']['timestamp']))
            # print(shipping_timestamp)
            shipping_provider = product_re['shipment']['provider']
            shipping_provider_id = product_re['shipment']['providerId']
            shipping_trackingNumber = product_re['shipment']['trackingNumber']
            # print(jsonpath.jsonpath(product_re,'$..shippingOrderNumber')[0])
            shipping_OrderNumber = jsonpath.jsonpath(product_re, '$..shippingOrderNumber') if jsonpath.jsonpath(
                product_re, '$..shippingOrderNumber') != False else ""
        else:
            shipping_timestamp = re.sub(r'Z', "", re.sub(r'T', " ", product_re['updateTimestamp']))
            shipping_provider = ''
            shipping_provider_id = ''
            shipping_trackingNumber = ''
            shipping_OrderNumber = ''

        # print(shipping_OrderNumber)
        # print(jsonpath.jsonpath(product_re,'$..refund'))

        if jsonpath.jsonpath(product_re, '$..refund'):

            refund_timestamp = re.sub(r'Z', "", re.sub(r'T', " ", product_re['refund']['timestamp']))
            refund_reason = product_re['refund']['reason']
            refund_by = product_re['refund']['by']
            refund_cost = product_re['refund']['cost']
            refund_price = product_re['refund']['price']
            refund_fraction = product_re['refund']['fraction']

            sql = "UPDATE jorder SET order_time = '%s',update_timestamp = '%s',order_status = '%s',store_id = '%s',product_id = '%s',transaction_id = '%s',customer_id = '%s',product_sku = '%s',product_unitPrice = %s,product_shippingPrice = %s,product_quantity = %s,order_country = '%s',order_origAmount = %s,order_price = %s,order_cost = %s,specialLogisticsPriceConditions = '%s',joomShippingPriceUsed = '%s',shipping_Method = '%s',shipping_timestamp = '%s',shipping_provider = '%s',shipping_provider_id = '%s',shipping_trackingNumber = '%s',shipping_OrderNumber = '%s',refund_timestamp = '%s',refund_reason = '%s',refund_by = '%s',refund_cost = %s,refund_price = %s,refund_fraction = '%s',note = '%s' WHERE order_id = '%s'" % \
                  (order_time, update_timestamp, order_status, store_id, product_id, transaction_id, customer_id,\
                   product_sku, product_unitPrice, \
                   product_shippingPrice, product_quantity, order_country, order_origAmount, order_price, order_cost,\
                   specialLogisticsPriceConditions, joomShippingPriceUsed, shipping_Method, shipping_timestamp, \
                   shipping_provider, shipping_provider_id, shipping_trackingNumber, shipping_OrderNumber,\
                   refund_timestamp, refund_reason, refund_by, refund_cost, refund_price, refund_fraction,"2", order_id)
            # print(sql)

        else:

            sql = "UPDATE jorder SET order_time = '%s',update_timestamp = '%s',order_status = '%s',store_id = '%s',product_id = '%s',transaction_id = '%s',customer_id = '%s',product_sku = '%s',product_unitPrice = %s,product_shippingPrice = %s,product_quantity = %s,order_country = '%s',order_origAmount = %s,order_price = %s,order_cost = %s,specialLogisticsPriceConditions = '%s',joomShippingPriceUsed = '%s',shipping_Method = '%s',shipping_timestamp = '%s',shipping_provider = '%s',shipping_provider_id = '%s',shipping_trackingNumber = '%s',shipping_OrderNumber = '%s' WHERE order_id = '%s'" % \
                  (order_time, update_timestamp, order_status, store_id, product_id, transaction_id, customer_id,\
                   product_sku, product_unitPrice,\
                   product_shippingPrice, product_quantity, order_country, order_origAmount, order_price, order_cost,\
                   specialLogisticsPriceConditions, joomShippingPriceUsed, shipping_Method, shipping_timestamp,\
                   shipping_provider, shipping_provider_id, shipping_trackingNumber, shipping_OrderNumber, order_id)
            # print(sql)
        # sql = "UPDATE shipping SET tracking_true = %s,delivered = %s,depth = '%s',tracking_id = '%s',trackingNumber = '%s',arrived = %s,passedCustoms = %s WHERE order_id = '%s'" % \
        #       (tracking_true, delivered, depth, tracking_id, trackingNumber, arrived, passedCustoms, order_id)
        # print(sql)
        try:
            print(order_id + "退款数据已经更新")
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()


