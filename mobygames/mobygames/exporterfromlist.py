import logging
import os
import re
import sys
import urllib

from platforms import Platforms

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor

from spiders.mobygames_spider import MobygamesSpider

# parsers a list of games titles, and sends the constructed urls 
# to mobygames spider for scraping
class ExporterFromList:

	global platforms
	platforms = Platforms()
        
	def __init__(self, titlesfile = None, platform = None, region = None):

		# set default encoding to utf8 for parsing and logging
		# utf-8 characters in console and files
		#
		reload(sys)
		sys.setdefaultencoding('utf8')
        
		configure_logging(install_root_handler=False)
		logging.basicConfig(
			filename='export.log',
			filemode = 'a',
			format='%(levelname)s: %(message)s',
			level=logging.INFO
		)
                				
		# identify platform
		#
		self.platform = platform
		if self.platform is None:
			logging.error('No platform found! Pass it as an argument.')
			return
		else:			
			platformId = platforms.getId(self.platform)
			if platformId is None:
				logging.error('Platform ' + self.platform + ' not supported.')
				return
						
		self.titlesfile = titlesfile
		self.region = region		
		if self.region is None:
			self.region = "Worldwide"
		
		if titlesfile:		
		
			titles = []
			urls = []
			
			with open( self.titlesfile ) as f:
				titles = f.read().splitlines()
				
			for title in titles:
				logging.debug('Submitting title:' + title )
				urls.append(
					'http://mobygames.com/search/quick' +
					'?q=' + title +
					'&p=' + platformId +
					'&search=Go'
					'&sFilter=1'
					'&sG=on'
					'&search_title=' + urllib.quote( title ) + 
					'&search_platform=' + urllib.quote(self.platform) +
					'&search_region=' + urllib.quote(self.region)
				)
				
			process = CrawlerProcess(get_project_settings())
			process.crawl(MobygamesSpider, start_urls=urls)
			process.start()									
		else:
			logging.warning('No file.')
			
	# strip all text in parentheses
	#
	def normalizeName(self,value):
		value = self.remove_parentheses(value)
		value = self.remove_brackets(value)
		return value.strip()
	
	# remove parentheses and text inside them
	def remove_parentheses(self,x):
		if '(' in x and ')' in x:
			x = re.sub('\(.*?\)','',x)
		return x

	# remove brackets and text inside them
	def remove_brackets(self,x):
		if '[' in x and ']' in x:
			x = re.sub('\[.*?\]','',x)
		return x
                                    		
                        			


