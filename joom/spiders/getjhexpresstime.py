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

    def start_requests(self):

        url = "http://ems.jhlems.com/ShipmentOrder/GetShipmentOrderByTrackNos?data="
        # url = "http://www.baidu.com"

        headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cache-Control": "max-age=0",
            # "Connection": "keep-alive",
            # "Host": "ems.jhlems.com",
            # "X-Requested-With": "XMLHttpRequest",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            # "Authorization": self.settings.get('JOOM_AUTH')
            # "Cookie": "culture=zh-CN; ASP.NET_SessionId=y2qqm41aoixfnn0dzz24slrk; __RequestVerificationToken=4ah8wrMYknRPk4HIX2yO98-hmLNon54T6hyDYQoBpDbpxHuezrH2TUEC1V8Zszj2kBD9F6iFUKsb2pAlF9lFbiHuOQyYjtl7HYfbm-_S6Vo1; .ASPXAUTH=BE46D38C43F686C74A4A80CDD90B9404BFE0039A8AD49A7AB568AE606EB6D8C66A5FCE03363E6111B620B98E73246817432C0B76091D6407F87F6C5DA2182BE1C513B88EB80C232CA4BBBC25E5B792DB368E97A4FB2D2CEAD193A54701E637BEBB5E80CC632474478331251260C24F21"
        }
        # cookies = "gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; login_js_cookie_phone_cookie=; order_data_js_cookie_get_custom_item=1; purchases_open_search_cookie=1; applylistshowset=1; applylistshowsetnum=10; XJFHPrompt_config_150769=1; purchaselistrowsPerPage_150769=50; purchaseLimit=0; order_data_js_cookie_isSyn=2; order_data_js_cookie_title_head_switch=1; XJFHPrompt_config_222014=1; purchaselistrowsPerPage_222014=500; order_data_js_cookie_orderbysVal_7=profit; order_data_js_cookie_orderbydacname_7=orderBysprofit; order_data_js_cookie_orderbydacnameval_7=up; lang=cn; order_data_js_cookie_orderbydacnameval_4=down; order_data_js_cookie_orderbysVal=platformIdshopIdorderFee; order_data_js_cookie_orderbydacname=orderBysplatformIdshopIdorderFee; order_data_js_cookie_orderbydacnameval=up; order_data_js_cookie_isImmediately=1; pickingListPrint_222014=%5B%7B%22name%22%3A%22orderId%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformOrderIdQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumberQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22salesRecordNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22shopName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22picture%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22supplierName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22sku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22skuQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22originSku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSkushop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformQuantityshop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22specifics%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22title%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22quantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22productUnit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22remark%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSku%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22buyerName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockRemark%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockPrint%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22countryNameCn%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22ItemId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22packageId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber1%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22warehouse%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22wstockQuantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22warehouseShelf%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22myLogisticsChannel%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22costPrice%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFee%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFeeO%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22profit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22purchaseName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22imageLarge%22%2C%22value%22%3A%22bigpic%22%7D%5D; goodsLimit=0; purchaselistrowsPerPage_191565=500; XJFHPrompt_config_191565=1; order_data_js_cookie_orderbysVal_undefined=paidTime; order_data_js_cookie_orderbydacname_undefined=orderByspaidTime; order_data_js_cookie_orderbydacnameval_undefined=up; order_data_js_cookie_orderbysVal_4=expressTime; order_data_js_cookie_orderbydacname_4=orderBysexpressTime; order_data_js_cookie_orderbysVal_3=stockSku; order_data_js_cookie_orderbydacname_3=orderBysstockSku; order_data_js_cookie_orderbydacnameval_3=down; signed=191565_d2fca9dca4b10fce3e24ce2f4feb7194; CRAWL_KANDENG_KEY=5%2FCNJ9PllrGrgYWbfj9LpQuWM3BVQLEUTBohyJPFyeooa8%2BgkBow1CKkIRRqrcjv8z27YPZo7%2BhybpnYp8fNhg%3D%3D; CustomitemsPurchaseflag=1; Merge_changeprint_191565=; PHPSESSID=l1v37tslhkq80o9vjp98ic8c54; MABANG_ERP_PRO_MEMBERINFO_LOGIN_COOKIE=MABANG_ERP_PRO_MEMBERINFO_LOGIN_191565; memberInfo=a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A11%3A%2215670629660%22%3Bs%3A8%3A%22password%22%3Bs%3A51%3A%22cd442mYboIVZApzNxYVC60CnlSpn6ZnFXXTK5Deu92m6ofzg4x8%22%3Bs%3A4%3A%22type%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sign%22%3Bs%3A39%3A%22191565_db5196565fb7e15caca92eafbb6eb5b0%22%3B%7D; order_rows_per_page_data_cookie=100; loginCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22191565%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22ecaf90da4c02f35b4adf3cefbed750a8%22%3B%7D"
        cookies = "culture=zh-CN; lang=en-US; __RequestVerificationToken=25ofBvt6URrCtYRNTcgNKHpq44EqtviKW7RKalD_nImvvSt25yn605o3wzHlc7mEOmRhbJo87z4hT9_j07Q9Wn4_64JzLby0T0ldsJ-uUs01; ASP.NET_SessionId=5frp53mluqze4qtmyibmizug; .ASPXAUTH=67ABF776D0B14642FD40C3B99D2B7C7BE2182B21A66662C3262E00400CE26DFDF3A135CFA9E74F84A6C879B52466295A9D278DEBA8A93B3C49825637FBFCDB9ACB666B9CF7E6825D41A075CAA4B638202C0245A4F065E0910357D96BFDD8375FE50C5E2C0FE9C20756FEBE17E8EE75D9"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

        # meta = {
        #     'dont_redirect': True,  # 禁止网页重定向
        #     'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        # }

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
        # print("123123")
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

        # 处理数据
        shipping_re = json.loads(response.text)
        # print(shipping_re)
        # 订单id
        # order_id = re.xpath('//*[@id="order-form"]/div[1]/div[2]/div[1]/div[1]/p/text()').extract()[0]
        # 物流单号
        tracking_number = shipping_re[0]['TrackingNumber']
        # 入库时间
        CheckInTime = shipping_re[0]['CheckInTime']
        # 出库时间
        # CheckOutTime = shipping_re[0]['CheckOutTime']
        # 服务商代码
        ServiceCode = shipping_re[0]['ServiceCode']
        # 处理地点
        CheckInCompany = shipping_re[0]['CheckInCompany']
        # 重量
        Weight = shipping_re[0]['Weight']
        # 合并单号
        ConsolidateNo = shipping_re[0]['ConsolidateNo']
        # 错误信息
        ErrorMsg = shipping_re[0]['ErrorMsg']

        # SQL 插入语句

        sql = "INSERT INTO jh_expresstime(tracking_number, CheckInTime, ServiceCode, CheckInCompany, Weight, ConsolidateNo, ErrorMsg) \
               VALUES ('%s', '%s', '%s','%s','%s','%s','%s')" % \
              (tracking_number, CheckInTime, ServiceCode, CheckInCompany, Weight, ConsolidateNo, ErrorMsg)
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


