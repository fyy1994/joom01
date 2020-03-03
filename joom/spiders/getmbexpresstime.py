# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
import time
from scrapy.selector import Selector


class GetmbexpresstimeSpider(scrapy.Spider):
    name = 'getmbexpresstime'
    # 域名要写对，要不就不写
    # allowed_domains = ['joom.com']



    def start_requests(self):

        url = "https://aamz.mabangerp.com/index.php?mod=order.detail&orderStatus=1&orderTable=2&tableBase=1&cMKey=MABANG_ERP_PRO_MEMBERINFO_LOGIN_222014&lang=cn&platformOrderId="

        headers = {
            "Sec-Fetch-Mode": "nested-navigate",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",

        }
        cookies = "lang=cn; signed=222014_00f6735cc675f0abb6f483d9913f72bf; gr_user_id=63993efb-e900-472c-9e8d-4d3e5c1832b2; stock_show_product_data_cookie=ico-minus-circle; employ_rows_per_page_data_cookie=10; stock_data_js_cookie_is_change_weight=1; stock_data_js_cookie_is_change_name=1; CRAWL_KANDENG_KEY=K6uqW0ZkQEouz0n1adoI%2FWqfFs2PbJ8%2BCpQKvtnzAvWpTX174VXBmq5L9cDOSOj%2Bm2IcDf7pRauH34yzR4OEyw%3D%3D; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; mabang_lite_rowsPerPage=500; PHPSESSID=gbtnacjhjolnnvb3cmcijbcbp0; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22222014%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%2282bc6a8ec7fca9d8d0d844f2882546e7%22%3B%7D; event_rember12_222014=0"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        # print(cookies)

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
        # sql = "SELECT order_id.order_id FROM order_id LEFT JOIN mb_expresstime ON mb_expresstime.order_id = order_id.order_id  WHERE TO_DAYS( NOW( ) ) - TO_DAYS( order_id.order_time ) <=10 AND mb_expresstime.order_id IS NULL"
        sql = "SELECT * FROM view_mb_express "
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
                yield scrapy.Request(url=url + order_id, cookies=cookies, headers=headers, callback=self.parse)

        except:
            print('Error: 数据查询错误')

        # 关闭数据库连接
        db.close()
        # yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)


    def parse(self, response):

        re = response
        # print(response.text)
        # print("2222222")

        # 订单状态
        order_st = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[1]/div[2]/p/text()').extract()[0]

        # 订单id
        order_id = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[1]/div[1]/p/text()').extract()[0]

        if order_st == '已发货':

            print(order_id)
            # 物流单号
            tracking_number = re.xpath('//*[@id="order-form"]/div[5]/div[2]/div[2]/div[1]/input/@value').extract()[0]
            # tracking_number = re.xpath('//*[@id="order-form"]/div[4]/div[2]/div[2]/div[1]/input/@value').extract()[0]
            # print(tracking_number)
            # 马帮发货时间
            expresstime = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[8]/div[2]/input/@value').extract()[0]
            # 马帮订单id
            mb_orderid = re.xpath('//*[@id="order-form"]/div[1]/div[1]/input[1]/@value').extract()[0]
            # print(mb_orderid)
            # print(order_st)

            # 传输数据
            mb_meta = {
                'order_id': order_id,
                'tracking_number': tracking_number,
                'order_st': order_st,
                'expresstime': expresstime,
                'mb_orderid': mb_orderid
                       }
            # 获取合并订单的sku
            # print(mb_meta)
            url = 'https://aamz.mabangerp.com/index.php?mod=order.findrelevantinfo'

            headers = {
                # "Accept": "application/json, text/javascript, */*; q=0.01",
                # "Accept-Encoding": "gzip, deflate, br",
                # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                # "Cache-Control": "no-cache",
                # "Connection": "keep-alive",
                # "Content-Type": "application/json; charset=UTF-8",

                # "Host": "aamz.mabangerp.com",
                # "Content-Length": "",
                # "X-Requested-With": "XMLHttpRequest",
                # "Referer": "https://aamz.mabangerp.com/index.php?mod=order.detail&platformOrderId=0O43LJNW&orderStatus=2&orderTable=2&tableBase=2&cMKey=MABANG_ERP_PRO_MEMBERINFO_LOGIN_191565&lang=cn",

                # 注意user-agent不要出现空格
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
            }

            # post请求数据
            data1 = {
                'orderId': mb_orderid,
                'type': '1',
                'tableBase': '2'
            }
            # cookies数据
            cookies = "lang=cn; signed=222014_00f6735cc675f0abb6f483d9913f72bf; gr_user_id=63993efb-e900-472c-9e8d-4d3e5c1832b2; stock_show_product_data_cookie=ico-minus-circle; employ_rows_per_page_data_cookie=10; stock_data_js_cookie_is_change_weight=1; stock_data_js_cookie_is_change_name=1; CRAWL_KANDENG_KEY=K6uqW0ZkQEouz0n1adoI%2FWqfFs2PbJ8%2BCpQKvtnzAvWpTX174VXBmq5L9cDOSOj%2Bm2IcDf7pRauH34yzR4OEyw%3D%3D; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; mabang_lite_rowsPerPage=500; PHPSESSID=gbtnacjhjolnnvb3cmcijbcbp0; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22222014%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%2282bc6a8ec7fca9d8d0d844f2882546e7%22%3B%7D; event_rember12_222014=0"
            cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

            # yield scrapy.Request(url=url, cookies=self.cookies, headers=headers, meta=mb_meta, callback=self.parse2)
            yield scrapy.FormRequest(url=url, cookies=cookies, formdata=data1, headers=headers, meta=mb_meta, callback=self.detail_parse)
        else:
            print(order_id + "订单状态为:" + order_st)

    def detail_parse(self, response):
        # print("3333333333333332")
        # 打开数据库连接
        db = pymysql.Connect(
            host='192.168.1.22',
            port=7306,
            user='root',
            passwd='123456',
            db='joom',
            charset='utf8'
        )
        #
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 获取合并订单信息数据
        re_list = json.loads(response.text)

        re = re_list['orderhtml']
        # print(re)
        # 接收传输的订单信息
        order_id = response.meta['order_id']
        tracking_number = response.meta['tracking_number']
        expresstime = response.meta['expresstime']

        sql = "INSERT INTO mb_expresstime(order_id, tracking_number, expresstime) \
                                       VALUES ('%s', '%s', '%s')" % \
              (order_id, tracking_number, expresstime)

        # print(sql)
        try:
            # 执行sql语句
            print("合并主订单 -- " + sql)
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except pymysql.Error as e:
            # 发生错误时回滚
            print("错误代码 %d: %s" % (e.args[0], e.args[1]))
            # print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            print(sql)
            db.rollback()
            print(order_id + "出现错误")


        # 合并订单列表
        hb_order_id_list = Selector(text=re).xpath('//a/text()').extract()

        # 判断是否是合并订单
        if hb_order_id_list:

            for row in hb_order_id_list:
                hb_order_id = row
                # print("24")
                # print(hb_order_id)
                sql = "INSERT INTO mb_expresstime(order_id, tracking_number, expresstime) \
                                   VALUES ('%s', '%s', '%s')" % \
                              (hb_order_id, tracking_number, expresstime)
                try:
                    print("   被合并订单 - " + sql)
                    # 执行sql语句
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                except:
                    print("err %s: " % sql)
                    f = open('123.txt', 'a')
                    f.writelines(repr(sql))
                    f.close()


                    # 发生错误时回滚
                    db.rollback()

        else:
            pass

        # 关闭数据库连接
        db.close()



