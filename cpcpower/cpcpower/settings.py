# -*- coding: utf-8 -*-

# Scrapy settings for cpcpower project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cpcpower'

SPIDER_MODULES = ['cpcpower.spiders']
NEWSPIDER_MODULE = 'cpcpower.spiders'

FILES_STORE = './files'

IMAGES_STORE = './files/images'

# 30 days of delay for images expiration
IMAGES_EXPIRES = 30

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cpcpower (+http://www.yourdomain.com)'
USER_AGENT = 'http://www.cpc-power.com'
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False
CONCURRENT_REQUESTS_PER_DOMAIN = 1 #    Default: 8

LOG_ENABLED = True
LOG_STDOUT = True
LOG_LEVEL = 'INFO'
LOG_FILE = './cpcpower.log'

# Disable Amazon S3 download handler
DOWNLOAD_HANDLERS = {
    's3': None,
        }


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

