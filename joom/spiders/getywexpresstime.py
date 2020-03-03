# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time


class GetywexpresstimeSpider(scrapy.Spider):
    name = 'getywexpresstime'
    # allowed_domains = ['track.yw56.com.cn/zh-CN']
    # 设置爬虫速度
    custom_settings = {'DOWNLOAD_DELAY': 0.5}
    # start_urls = ['http://track.yw56.com.cn/zh-CN']
    # handle_httpstatus_list = [301,302,204,206,404,500]

    def start_requests(self):
        url = 'https://track.yw56.com.cn/zh-CN/'

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            # "Connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "track.yw56.com.cn",
            "upgrade-insecure-requests": "1",
            "TE": "Trailers",
            # 注意user-agent不要出现空格
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
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
        sql = "SELECT * FROM view_yw_express"
        # sql = "SELECT trackingNumber FROM wuliu1"

        # cookies = "_ga=GA1.3.56859337.1548406740; pgv_pvi=8394121216; _qddaz=QD.4p7zxi.gqau5k.jrbte770; locale=zh-CN; Hm_lvt_842afda4ea3bdf5a2ac6bbb84f564374=1573521816,1573799259,1574818446,1574991429; Hm_lpvt_842afda4ea3bdf5a2ac6bbb84f564374=1574991446"
        # cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

        i = 0
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            for row in results:
                i = i + 1
                print(i)
                tr_Number = row[0]
                print(tr_Number)
                data = {
                    'InputTrackNumbers': tr_Number
                }
                # print(data)
                yield scrapy.FormRequest(url=url, headers=headers, formdata=data, callback=self.parse)

        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()

    def parse(self, response):
        # print(response.text)
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
        # if response.text:
        # print("111111111111111111111111111111")
        # else:
        #     print("222222222222222222222222222222")

        # 处理数据
        shipping_re = response
        # print(shipping_re.text)

        if shipping_re.xpath('//*[@id="accordion"]/div/div[1]/div[1]/div[2]/div/a/@aria-controls').extract():
        # print(shipping_re)
        # 物流单号
        # tracking_number = shipping_re.xpath('//*[@id="accordion"]/div/div[1]/div[1]/div[2]/h4/text()').extract()[0]

            tracking_number = shipping_re.xpath('//*[@id="accordion"]/div/div[1]/div[1]/div[2]/div/a/@aria-controls').extract()[0]
            # 入库时间
            CheckInTime = shipping_re.xpath('//*[@role="tabpanel"]/table/tbody/tr[last()]/td[1]/text()').extract()[0]
            # # 转运单号
            zhunyun_number = shipping_re.xpath('//*[@id="accordion"]/div/div[1]/div[1]/div[2]/h4/small/text()').extract()[0]

            # SQL 插入语句

            sql = "INSERT INTO yw_expresstime(tracking_number, CheckInTime, zhunyun_number) \
                   VALUES ('%s', '%s','%s')" % \
                  (tracking_number, CheckInTime, zhunyun_number)

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
