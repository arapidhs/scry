# Scrapy settings for mobygames project

BOT_NAME = 'mobygames'

SPIDER_MODULES = ['mobygames.spiders']

NEWSPIDER_MODULE = 'mobygames.spiders'

ITEM_PIPELINES = {
	'scrapy.pipelines.images.ImagesPipeline': 1,
	'mobygames.duplicates.DuplicatesPipeline': 2,
	'mobygames.pipelines.MobygamesPipeline': 3

	}
	
FILES_STORE = './files/sega-mega-drive-missing'

IMAGES_STORE = './files/sega-mega-drive-missing/images'

# max number of screenshots to download per game
MAX_SCREENSHOTS = 6

# Use FEED_EXPORT_FIELDS option to define 
# fields to export and their order.
# 	
FEED_EXPORT_FIELDS = [
	"url",			"title",		"platform", 
	"region", 		"publisher", 	"developer", 
	"date", 		"rating", 		"genre", 
	"perspective", 	"theme", 		"sport",
	"misc", 		"group", 		"description", 
	"criticScore",	"userScore", 	"images",
	"image_urls",	"file",			"file_urls",
	"visual",		"presentation",	"pacing", 
	"vehicular",	"gameplay", 	"narrative",	
	"addon",	"educational"
]

# 30 days of delay for images expiration
IMAGES_EXPIRES = 60

#IMAGES_THUMBS = {
#	'small': (50, 50),
#	'big': (270, 270),
#	}

# Download and traffic settings.
# Limit concurrent requests and add a 
# download delay to minimize hammering.

# drop small images
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

USER_AGENT = 'http://www.mobygames.com'
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False
CONCURRENT_REQUESTS_PER_DOMAIN = 8 # 	Default: 8

LOG_ENABLED = True
LOG_STDOUT = False
LOG_LEVEL = 'INFO'
LOG_FILE = './export.log'

# Disable Amazon S3 download handler
DOWNLOAD_HANDLERS = {
    's3': None,
    }
    
# Disable Telnet console
EXTENSIONS = {
   'scrapy.telnet.TelnetConsole': None
}


