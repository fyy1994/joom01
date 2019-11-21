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
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cache-Control": "max-age=0",
            # "Connection": "keep-alive",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Host": "aamz.mabangerp.com",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            # "X-Requested-With": "XMLHttpRequest",
        }
        # cookies = "gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; login_js_cookie_phone_cookie=; order_data_js_cookie_get_custom_item=1; purchases_open_search_cookie=1; applylistshowset=1; applylistshowsetnum=10; XJFHPrompt_config_150769=1; purchaselistrowsPerPage_150769=50; purchaseLimit=0; order_data_js_cookie_isSyn=2; order_data_js_cookie_title_head_switch=1; XJFHPrompt_config_222014=1; purchaselistrowsPerPage_222014=500; order_data_js_cookie_orderbysVal_7=profit; order_data_js_cookie_orderbydacname_7=orderBysprofit; order_data_js_cookie_orderbydacnameval_7=up; lang=cn; order_data_js_cookie_orderbydacnameval_4=down; order_data_js_cookie_orderbysVal=platformIdshopIdorderFee; order_data_js_cookie_orderbydacname=orderBysplatformIdshopIdorderFee; order_data_js_cookie_orderbydacnameval=up; order_data_js_cookie_isImmediately=1; pickingListPrint_222014=%5B%7B%22name%22%3A%22orderId%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformOrderIdQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumberQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22salesRecordNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22shopName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22picture%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22supplierName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22sku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22skuQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22originSku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSkushop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformQuantityshop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22specifics%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22title%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22quantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22productUnit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22remark%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSku%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22buyerName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockRemark%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockPrint%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22countryNameCn%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22ItemId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22packageId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber1%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22warehouse%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22wstockQuantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22warehouseShelf%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22myLogisticsChannel%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22costPrice%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFee%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFeeO%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22profit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22purchaseName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22imageLarge%22%2C%22value%22%3A%22bigpic%22%7D%5D; goodsLimit=0; purchaselistrowsPerPage_191565=500; XJFHPrompt_config_191565=1; order_data_js_cookie_orderbysVal_undefined=paidTime; order_data_js_cookie_orderbydacname_undefined=orderByspaidTime; order_data_js_cookie_orderbydacnameval_undefined=up; order_data_js_cookie_orderbysVal_4=expressTime; order_data_js_cookie_orderbydacname_4=orderBysexpressTime; order_data_js_cookie_orderbysVal_3=stockSku; order_data_js_cookie_orderbydacname_3=orderBysstockSku; order_data_js_cookie_orderbydacnameval_3=down; signed=191565_d2fca9dca4b10fce3e24ce2f4feb7194; CRAWL_KANDENG_KEY=5%2FCNJ9PllrGrgYWbfj9LpQuWM3BVQLEUTBohyJPFyeooa8%2BgkBow1CKkIRRqrcjv8z27YPZo7%2BhybpnYp8fNhg%3D%3D; CustomitemsPurchaseflag=1; Merge_changeprint_191565=; PHPSESSID=l1v37tslhkq80o9vjp98ic8c54; MABANG_ERP_PRO_MEMBERINFO_LOGIN_COOKIE=MABANG_ERP_PRO_MEMBERINFO_LOGIN_191565; memberInfo=a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A11%3A%2215670629660%22%3Bs%3A8%3A%22password%22%3Bs%3A51%3A%22cd442mYboIVZApzNxYVC60CnlSpn6ZnFXXTK5Deu92m6ofzg4x8%22%3Bs%3A4%3A%22type%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sign%22%3Bs%3A39%3A%22191565_db5196565fb7e15caca92eafbb6eb5b0%22%3B%7D; order_rows_per_page_data_cookie=100; loginCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22191565%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22ecaf90da4c02f35b4adf3cefbed750a8%22%3B%7D"
        cookies = "gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; lang=cn; stock_show_product_data_cookie=ico-minus-circle; stock_data_js_cookie_is_change_weight=1; mabang_lite_rowsPerPage=500; stock_data_js_cookie_is_change_name=1; order_data_js_cookie_orderErrorbysVal=paidTime; order_data_js_cookie_orderErrorbydacname=orderByspaidTime; order_data_js_cookie_orderErrorbydacnameval=down; order_data_js_cookie_isSyn=2; employ_rows_per_page_data_cookie=50; order_data_js_cookie_isImmediately=1; signed=222014_00f6735cc675f0abb6f483d9913f72bf; PHPSESSID=gjgkl12ntct9knahgq66qtlks1; event_rember12_222014=0; CRAWL_KANDENG_KEY=K6uqW0ZkQEouz0n1adoI%2FWqfFs2PbJ8%2BCpQKvtnzAvWpTX174VXBmq5L9cDOSOj%2Bm2IcDf7pRauH34yzR4OEyw%3D%3D; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22222014%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22f1c7edfb07a416030a0f976bac902add%22%3B%7D"
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

        # 处理数据
        # 订单id
        order_id = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[1]/div[1]/p/text()').extract()[0]
        # 物流单号
        tracking_number = re.xpath('//*[@id="order-form"]/div[5]/div[2]/div[2]/div[1]/input/@value').extract()[0]
        # 订单状态
        order_st = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[1]/div[2]/p/text()').extract()[0]
        # 马帮发货时间
        expresstime = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[8]/div[2]/input/@value').extract()[0]
        # 马帮订单id
        mb_orderid = re.xpath('//*[@id="order-form"]/div[1]/div[1]/input[1]/@value').extract()[0]
        # print(mb_orderid)
        # print(order_st)

        if order_st == '已发货':
            # 传输数据
            mb_meta = {
                'order_id': order_id,
                'tracking_number': tracking_number,
                'order_st': order_st,
                'expresstime': expresstime,
                'mb_orderid': mb_orderid
                       }
            # 获取合并订单的sku
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
            cookies = "gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; lang=cn; stock_show_product_data_cookie=ico-minus-circle; stock_data_js_cookie_is_change_weight=1; mabang_lite_rowsPerPage=500; stock_data_js_cookie_is_change_name=1; order_data_js_cookie_orderErrorbysVal=paidTime; order_data_js_cookie_orderErrorbydacname=orderByspaidTime; order_data_js_cookie_orderErrorbydacnameval=down; order_data_js_cookie_isSyn=2; employ_rows_per_page_data_cookie=50; order_data_js_cookie_isImmediately=1; signed=222014_00f6735cc675f0abb6f483d9913f72bf; PHPSESSID=gjgkl12ntct9knahgq66qtlks1; event_rember12_222014=0; CRAWL_KANDENG_KEY=K6uqW0ZkQEouz0n1adoI%2FWqfFs2PbJ8%2BCpQKvtnzAvWpTX174VXBmq5L9cDOSOj%2Bm2IcDf7pRauH34yzR4OEyw%3D%3D; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22222014%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22f1c7edfb07a416030a0f976bac902add%22%3B%7D"
            cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

            # yield scrapy.Request(url=url, cookies=self.cookies, headers=headers, meta=mb_meta, callback=self.parse2)
            yield scrapy.FormRequest(url=url, cookies=cookies, formdata=data1, headers=headers, meta=mb_meta, callback=self.detail_parse)
        else:
            pass

    def detail_parse(self, response):
        # print("2")
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

        # 接收传输的订单信息
        order_id = response.meta['order_id']
        tracking_number = response.meta['tracking_number']
        expresstime = response.meta['expresstime']

        sql = "INSERT INTO mb_expresstime(order_id, tracking_number, expresstime) \
                                       VALUES ('%s', '%s', '%s')" % \
              (order_id, tracking_number, expresstime)
        try:
            # 执行sql语句
            print("合并主订单 -- " + sql)
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()


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
                    # 发生错误时回滚
                    db.rollback()

        else:
            pass

        # 关闭数据库连接
        db.close()



