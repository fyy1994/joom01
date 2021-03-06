# -*- coding: utf-8 -*-

# Scrapy settings for joom project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'joom'

SPIDER_MODULES = ['joom.spiders']
NEWSPIDER_MODULE = 'joom.spiders'

LOG_LEVEL = 'WARNING'

FEED_EXPORT_ENCODING = 'utf-8'

# 限制爬虫速度
# DOWNLOAD_DELAY = 1
# RANDOMIZE_DOWNLOAD_DELAY = True


JOOM_AUTH = 'Bearer SEV0001MTU3NDAzNzkzNXxDQWMwbkVmVV9QcmN4RlVFNlBidE5iQmQ3OEt0OEtoUkJvcVpESlJIakNGWUlwYjlmcmNQMlFFMTBON3k5Rmlfc1F3RkFQR2F0MTRLajdVcmNac1pmRVA5aW82X1RpaUJVUm9tdlc2U2I4OEFGRTdsRl91Y1BMVHZCWjJZQ0t4aEdYcnhwUkwxUHltTVVYb3FLYU5qYWg1QjVYcEhnNDF6VEI5VF9FZThRanBZRFlnY1VCMTAtN3ZTc0RyWk5lMWtCbUtTaTFsbU5SbGg0Tmdkb0tsZnVBPT18tc4WkNuEmtbxagwYQ0cBYmedqaxW9F4csN9oKQmMwqs='


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'joom (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'joom.middlewares.JoomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'joom.middlewares.JoomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'joom.pipelines.JoomPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
