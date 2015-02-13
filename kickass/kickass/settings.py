# Scrapy settings for kickass project

BOT_NAME = 'kickass'

SPIDER_MODULES = ['kickass.spiders']
NEWSPIDER_MODULE = 'kickass.spiders'
ITEM_PIPELINES = ['kickass.pipelines.TorrentPipeline',]

# Download and traffic settings.
# Limit concurrent requests and add a 
# download delay to minimize hammering.
USER_AGENT = 'http://www.kickass.to)'
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = False
CONCURRENT_REQUESTS_PER_DOMAIN = 1 # 	Default: 8
#SCHEDULER = 'scrapy.core.scheduler.Scheduler'

# Log Settings
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG' #	Levels: CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_FILE = './kickass.log'
