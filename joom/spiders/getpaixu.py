# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import FormRequest


class GetpaixuSpider(scrapy.Spider):
    name = 'getpaixu'
    allowed_domains = ['joom.com']
    # start_urls = ['http://joom.com/']
    handle_httpstatus_list = [404]


    def start_requests(self):

        url = "https://www.joom.com/en/search/q."
        keyword = 'bluetooth'
        qqq = 'https://api.joom.com/1.1/search/content?currency=USD&language=en-US&_=jzdy512h'
        headers = {

            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            # "Content-Type":"application/json",
            # "Origin": "https: // www.joom.com",
            # "Host": "https: // www.joom.com",
            # "Referer": "https: // www.joom.com / en / search / q.bluetooth",
            # "X - API - Token": "ARjbh0l7Rhm2xmHVbvQxdyYyF6LS2PCt",
            # "X - OSType": "Windows",
            # "X - Version": "2.100.0",
            # "Authorization": "Bearer SEV0001MTU2NTc2NDAwM3xwM0xjYVI4NGRfbkJPSWN2UW9aVVJMTEZHTTlWd1g1VDhvem1tdU5CVkJ4bUVibUk0OENRWHFfdGc0RHRzUF9jcTIwdGs3Wnl3Nm9vcU5QUzR4N3NrVHp2REhvV0p2cHVydTFlbk1oOEFsYVo1dUpWVm0za05Eb3dKb3poQTZFQmpTTGhkeGdiMGNQbEJQRnVkY0RZa0JUcUQtWnVZYVVueHNpQXVTWmt2cTVMQ3c4PXzdkHDTW7ebu9uDNk9VMYBNDYyJOMM4f6D6LARwQ7ooPw =="

            # "Authorization": "Bearer SEV0001MTU2NDYyNDY2NHxad0Y5R21IRXA5b05ZRDJ4WDBRSUJnVXZZekRaeTNTcFBHWGtpclRDbGlJUUdsWXBKR1ZsMGJiZHhMV200MU5CNEpoMXFGR2VwVUp0bVliUEZSZDh4ZmVoOWZIckpPU1FKcDBXWWlxNjA5dmxfbDZER1dqM2ROaVV5SGpkdXRxSUhGWElzQkUzWW96bkN5LTRSUEdKODJnV3JraV9KS3NxSjFtNDRwc2ctOWRSTWNqYVlZQzF0ak9WV0o0bFBoVjZxX24yS0lBc1I4ZDlmTFBSQUZYQXzdAUMh7tF91g_u_2iK6eq5QlXqtRKfsx8Z47DqiMD_jA==",
        }
        form_data = {"query":"bluetooth","appearance":{"productColumns":12},"count":36}
        formdata = '{"query":"bluetooth","appearance":{"productColumns":12},"count":36}'
        print(json.dumps(form_data))
        # yield scrapy.Request(url=url + keyword, headers=headers, callback=self.parse)
        yield scrapy.FormRequest(url=qqq, body=json.dumps(form_data), headers=headers, method="POST", callback=self.parse)
        # yield scrapy.FormRequest(url=qqq, body=json.dumps(formdata), headers=headers, method="POST", callback=self.parse,dont_filter=True)




    def parse(self, response):

        print(11)
        print(response)






