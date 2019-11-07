# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import pymysql
import re
from scrapy.selector import Selector


class GetrefundSpider(scrapy.Spider):
    name = 'getrefund'
    allowed_domains = ['joom']
    start_urls = ['http://joom/']


    def start_requests(self):

        url = "https://aamz.mabangerp.com/index.php?mod=paypal.dosearchpaypalrefund"

        headers = {
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent ": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            # "Content-Type": "application/json;charset=utf-8",
            "Host": "aamz.mabangerp.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            # "Authorization": self.settings.get('JOOM_AUTH')
            # "Cookie": "gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; login_js_cookie_phone_cookie=; order_data_js_cookie_get_custom_item=1; purchases_open_search_cookie=1; applylistshowset=1; applylistshowsetnum=10; XJFHPrompt_config_150769=1; purchaselistrowsPerPage_150769=50; purchaseLimit=0; order_data_js_cookie_isSyn=2; order_data_js_cookie_title_head_switch=1; XJFHPrompt_config_222014=1; purchaselistrowsPerPage_222014=500; order_data_js_cookie_orderbysVal_7=profit; order_data_js_cookie_orderbydacname_7=orderBysprofit; order_data_js_cookie_orderbydacnameval_7=up; lang=cn; order_data_js_cookie_orderbydacnameval_4=down; order_data_js_cookie_orderbysVal=platformIdshopIdorderFee; order_data_js_cookie_orderbydacname=orderBysplatformIdshopIdorderFee; order_data_js_cookie_orderbydacnameval=up; order_data_js_cookie_isImmediately=1; pickingListPrint_222014=%5B%7B%22name%22%3A%22orderId%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformOrderIdQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumberQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22salesRecordNumber%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22shopName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22picture%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22supplierName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22sku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22skuQrcode%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22originSku%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSkushop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22platformQuantityshop%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22specifics%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22title%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22quantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22productUnit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22remark%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22platformSku%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22buyerName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockRemark%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22stockPrint%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22countryNameCn%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22ItemId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22packageId%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22trackNumber1%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22warehouse%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22wstockQuantity%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22warehouseShelf%22%2C%22value%22%3A1%7D%2C%7B%22name%22%3A%22myLogisticsChannel%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22costPrice%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFee%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22orderFeeO%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22profit%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22purchaseName%22%2C%22value%22%3A2%7D%2C%7B%22name%22%3A%22imageLarge%22%2C%22value%22%3A%22bigpic%22%7D%5D; goodsLimit=0; purchaselistrowsPerPage_191565=500; XJFHPrompt_config_191565=1; order_data_js_cookie_orderbysVal_undefined=paidTime; order_data_js_cookie_orderbydacname_undefined=orderByspaidTime; order_data_js_cookie_orderbydacnameval_undefined=up; order_data_js_cookie_orderbysVal_4=expressTime; order_data_js_cookie_orderbydacname_4=orderBysexpressTime; order_data_js_cookie_orderbysVal_3=stockSku; order_data_js_cookie_orderbydacname_3=orderBysstockSku; order_data_js_cookie_orderbydacnameval_3=down; cKey=MABANG_ERP_PRIVATE_LOGIN_169040_191565_M0010819; order_rows_per_page_data_cookie=500; signed=191565_d2fca9dca4b10fce3e24ce2f4feb7194; CRAWL_KANDENG_KEY=5%2FCNJ9PllrGrgYWbfj9LpQuWM3BVQLEUTBohyJPFyeooa8%2BgkBow1CKkIRRqrcjv8z27YPZo7%2BhybpnYp8fNhg%3D%3D; MABANG_ERP_PRO_MEMBERINFO_LOGIN_COOKIE=MABANG_ERP_PRO_MEMBERINFO_LOGIN_191565; loginCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22191565%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22926e8038593181f22ead72c5e3d6bf70%22%3B%7D; memberInfo=a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A11%3A%2215670629660%22%3Bs%3A8%3A%22password%22%3Bs%3A51%3A%220986dKVK%2FPsDG4jfIwOLCfSRgV4EzEr%2FswamKOA5Y%2Ba0CN935%2B4%22%3Bs%3A4%3A%22type%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22sign%22%3Bs%3A39%3A%22191565_43b705d0cf51c0cc54245749ab5249dc%22%3B%7D; CustomitemsPurchaseflag=1; PHPSESSID=023ifsus597uo44ian8e0e4c57"
        }
        cookies ="gr_user_id=493499a8-83fc-4e47-87c3-08b1ded6df3c; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; lang=cn; stock_show_product_data_cookie=ico-minus-circle; stock_data_js_cookie_is_change_weight=1; mabang_lite_rowsPerPage=500; stock_data_js_cookie_is_change_name=1; order_data_js_cookie_orderErrorbysVal=paidTime; order_data_js_cookie_orderErrorbydacname=orderByspaidTime; order_data_js_cookie_orderErrorbydacnameval=down; order_data_js_cookie_isSyn=2; matching_product_page_cookie=50; employ_rows_per_page_data_cookie=50; order_data_js_cookie_isImmediately=1; cKey=MABANG_ERP_PRIVATE_LOGIN_169040_191565_M0010819; signed=191565_d2fca9dca4b10fce3e24ce2f4feb7194; CRAWL_KANDENG_KEY=5%2FCNJ9PllrGrgYWbfj9LpQuWM3BVQLEUTBohyJPFyeooa8%2BgkBow1CKkIRRqrcjv8z27YPZo7%2BhybpnYp8fNhg%3D%3D; event_rember12_191565=0; PHPSESSID=ivn9o3vsap0hggdgo8bv05c7i2; loginLiteCookie=a%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22191565%22%3Bs%3A9%3A%22passsword%22%3Bs%3A32%3A%22f00a0213165a8469d9b1c59fcc165b16%22%3B%7D"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        # print(cookies)

        # # 打开数据库连接
        # db = pymysql.Connect(
        #     host='192.168.1.22',
        #     port=7306,
        #     user='root',
        #     passwd='123456',
        #     db='joom',
        #     charset='utf8'
        # )
        # # 使用cursor()方法获取操作游标
        # cursor = db.cursor()
        #
        # # SQL 查询还没有查询物流信息语句
        # sql = "SELECT shipping.order_id FROM shipping LEFT JOIN shipping_time ON shipping.order_id = shipping_time.order_id WHERE depth = 60 AND shipping_time.order_id IS NULL"
        # i = 0
        #
        # try:
        #     # 执行SQL语句
        #     cursor.execute(sql)
        #     # 获取所有记录列表
        #     results = cursor.fetchall()
        #     for row in results:
        #         i = i + 1
        #         print(i)
        #         order_id = row[0]
        #         # 链接字符串
        #         # print(url + fname)
        #         yield scrapy.Request(url=url + order_id, headers=headers, callback=self.parse)
        #
        # except:
        #     print('Error: 数据查询错误')
        #
        # # 关闭数据库连接
        # db.close()
        yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # 获取到退款数据
        re=response.text
        re_list=re.encode('utf8').decode('unicode_escape')

        # print(re_list)

        shipping_re = json.loads(re)
        delivered = shipping_re['message']

        print(delivered)

        # order_id_list = delivered.xpath('//strong/a/text()').extract()
        # for order_id in order_id_list:
        #     order = order_id
        #     print(order)


        # order_id_list = Selector(text=delivered).xpath('//span[@class="label label-platform label-joom"]/text()').extract()
        # 订单编号
        order_id_list = Selector(text=delivered).xpath('//strong/a/text()').extract()
        # 订单时间
        order_time_list = Selector(text=delivered).xpath('//span[@class="text-default pull-right"]/text()').extract()
        # 退款时间
        refund_time_list = Selector(text=delivered).xpath('//p[@data-original-title="退款时间"]/text()').extract()
        # 退款金额
        refund_m_list = Selector(text=delivered).xpath('///tr[@class="content"]/td[4]/text()').extract()
        hh = re.sub(r'USD', "", refund_m_list[0])
        print(order_id_list)
        print(order_time_list)
        print(refund_time_list)
        print(refund_m_list)
        print(hh)











