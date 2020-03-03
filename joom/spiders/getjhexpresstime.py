# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time


class GetjhexpresstimeSpider(scrapy.Spider):
    name = 'getjhexpresstime'
    allowed_domains = ['ems.jhlems.com']

    # start_urls = ['http://ems.jhlems.com/ShipmentOrder/GetShipmentOrderByTrackNos?data=JM1931101288017549']
    # handle_httpstatus_list = [301,302,204,206,404,500]
    # 设置不同的管道
    custom_settings = {
        'ITEM_PIPELINES': {'joom.pipelines.GetjhexpresstimePipeline': 301},
    }


    def start_requests(self):

        url = "http://ems.jhlems.com/ShipmentOrder/GetShipmentOrderByTrackNos?data="
        # url = "http://www.baidu.com"

        aa = input("输入cookies:")
        headers = {
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
        }
        cookies = aa
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

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
        # sql = "SELECT shipping_trackingNumber FROM jorder WHERE shipping_provider = 'Joom Logistics' AND TO_DAYS( NOW( ) ) - TO_DAYS( jorder.shipping_timestamp ) <= 10"
        sql = "SELECT * FROM view_jh_express"
        # sql = "SELECT * FROM view_jh_express"
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
                yield scrapy.Request(url=url + order_id, cookies=cookies, callback=self.parse)

        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()
        # yield scrapy.Request(url=url, headers=headers,cookies= cookies, callback=self.parse)
        # yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):

        if len(response.text) > 3:

            # 处理数据
            shipping_re = json.loads(response.text)
            # print(shipping_re)
            # shipping_time = shipping_re[0]['CheckInTime']
            # # print(shipping_time)
            # # 判断是否有物流信息
            # if shipping_time != '':

            shipping = {}
            # 物流单号
            shipping['tracking_number'] = shipping_re[0]['TrackingNumber']
            # 入库时间
            shipping['CheckInTime'] = shipping_re[0]['CheckInTime']
            # 出库时间
            # CheckOutTime = shipping_re[0]['CheckOutTime']
            # 服务商代码
            shipping['ServiceCode'] = shipping_re[0]['ServiceCode']
            # 处理地点
            shipping['CheckInCompany'] = shipping_re[0]['CheckInCompany']
            # 重量
            shipping['Weight'] = shipping_re[0]['Weight']
            # 合并单号
            shipping['ConsolidateNo'] = shipping_re[0]['ConsolidateNo']
            # 错误信息
            shipping['ErrorMsg'] = shipping_re[0]['ErrorMsg']

            yield shipping