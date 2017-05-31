import sys
import scrapy
import logging
import re
import urlparse
import string
import xml.etree.ElementTree as ET

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from collections import defaultdict

from mobygames.items import MobygamesItem
from mobygames.loaders import MobyLoader
from mobygames.platforms import Platforms


class MobygamesSpider(Spider):

	global platforms 
	
	platforms = Platforms()	
	
	name = "mobygames"
	
	allowed_domains = [
		"mobygames.com"
	]



	def __init__(self, *args, **kwargs): 

		super(MobygamesSpider, self).__init__(*args, **kwargs)
		
		# set default encoding to utf8 for parsing and logging
		# utf-8 characters in console and files
		#
		reload(sys)
		sys.setdefaultencoding('utf8')
		
		self.items = []
		
		if 'start_urls' in kwargs:
			self.start_urls = list(kwargs['start_urls'])
		elif 'title' in kwargs:			
		
			logging.info('Running spider with:' + str(kwargs))
			
			platform = platforms.getId( kwargs['platform'] )
			title = kwargs['title']
			
			logging.info('Platform ID:' + platform)
			
			region = 'Worldwide'
			if 'region' in kwargs.keys():
				region = kwargs['region']

			romname = ''
			if 'romname' in kwargs.keys():			
				romname = kwargs['romname']
			
			logging.info('Platform:' + self.platform)
			logging.info('Region:' + region)
			
			url = 'http://mobygames.com/search/quick' + \
					'?q=' + self.title + \
					'&p=' + self.platform + \
					'&search=Go' + \
					'&sFilter=1' + \
					'&sG=on' + \
					'&search_title=' + self.title + \
					'&search_platform=' + self.platform + \
					'&search_region=' + self.region
					
			if romname != '':
				url +=	'&romname=' + romname
			self.start_urls = [ url ]
			
			logging.info('Parsing URL:' + url)

		else:
			return
		


	# parse search results until a link matches title
	#
	def parse(self, response):

		self.crawler.stats.inc_value('games_crawled')
		
		parsed = urlparse.urlparse(response.url)	
		search_params = urlparse.parse_qs(parsed.query)
		search_title = search_params['search_title'][0]
		search_platform = search_params['search_platform'][0]
		search_region = search_params['search_region'][0]
		
		# store the original title criteria
		# before striiping and normalizing it for search
		#
		orig_title = search_title
		
		romname = ''
		
		if 'romname' in search_params.keys():
			romname = search_params['romname'][0]
		
		if ', The' in search_title:
			search_title = 'The ' + search_title.replace(", The","")

		if ', A' in search_title:
			search_title = 'A ' + search_title.replace(", A","")

				
		logging.info('Searching for:' + orig_title)
		
		selector = Selector(response) 
		
		titles = selector.css('.searchTitle').xpath('./a')
		aka_title = selector.css('.searchTitle').xpath('./em/following-sibling::text()[1]').extract_first()
		if ( aka_title ):
			aka_title = self.remove_parentheses(aka_title)
			aka_title =  filter(str.isalnum, aka_title.encode('utf-8')).lower()
			
		filtered_search_title = filter(str.isalnum, search_title.encode('utf-8')).lower()
		
		for t in titles:
		
			title = t.xpath('text()').extract_first()
			title = filter(str.isalnum, title.encode('utf-8')).lower()
			# strip whitespace, copare lower case title
			#
			if title == filtered_search_title 	or aka_title == filtered_search_title:
				logging.debug("Title found:" + title)
				item = MobygamesItem()				
				item['title'] = orig_title
				item['search_title'] = search_title
				item['search_platform'] = search_platform
				item['search_region'] = search_region
				item['url'] = t.xpath('./@href').extract_first()
				
				if romname != '':
					item['romname'] = romname

				self.logger.debug('Item:' + str(item))
				self.crawler.stats.inc_value('games_found')

				# match found return a new request to parse game page
				#
				request = scrapy.Request("http://mobygames.com" + item['url'],
					callback=self.parse_game)
				request.meta['item'] = item
				return request
			else:
				# log non matching search result
				#
				logging.debug("Skipping result::" + title)

		# if code reaches here, title was not found
		# and a a request was not returned
		#		
		logging.warning('Title not found:' +  search_title + ":" + search_region)
		self.crawler.stats.inc_value('games_not_found')

		
				
	def parse_game(self, response):		
	
		item = response.meta['item'] 
		logging.debug('Parsing ' + item['search_title'] + ' details.')
		
		l = MobyLoader(item, response=response) 
		l.add_xpath('platform', '//h1[contains(@class,"niceHeaderTitle")][1]/small/a/text()') 
		l.add_xpath('platforms', '//*[@id="coreGameRelease"]/div[.="Also For"]/following-sibling::div[1]//a/text()') 
		l.add_xpath('genre', '//*[@id="coreGameGenre"]/div/div[.="Genre"]/following-sibling::div[1]//a/text()') 
		l.add_xpath('presentation','//*[@id="coreGameGenre"]/div/div[.="Presentation"]/following-sibling::div[1]//a/text()')
		l.add_xpath('perspective','//*[@id="coreGameGenre"]/div/div[.="Perspective"]/following-sibling::div[1]//a/text()')
		l.add_xpath('pacing','//*[@id="coreGameGenre"]/div/div[.="Pacing"]/following-sibling::div[1]//a/text()')
		l.add_xpath('visual','//*[@id="coreGameGenre"]/div/div[.="Visual"]/following-sibling::div[1]//a/text()')
		l.add_xpath('vehicular','//*[@id="coreGameGenre"]/div/div[.="Vehicular"]/following-sibling::div[1]//a/text()')
		l.add_xpath('gameplay','//*[@id="coreGameGenre"]/div/div[.="Gameplay"]/following-sibling::div[1]//a/text()')
		l.add_xpath('setting','//*[@id="coreGameGenre"]/div/div[.="Setting"]/following-sibling::div[1]//a/text()')
		l.add_xpath('sport','//*[@id="coreGameGenre"]/div/div[.="Sport"]/following-sibling::div[1]//a/text()')
		l.add_xpath('theme','//*[@id="coreGameGenre"]/div/div[.="Theme"]/following-sibling::div[1]//a/text()')
		l.add_xpath('misc','//*[@id="coreGameGenre"]/div/div[.="Misc"]/following-sibling::div[1]//a/text()')
		l.add_xpath('criticScore','//div[contains(@class,"scoreBoxBig")]/text()')
		l.add_xpath('userScore','//div[contains(@class,"scoreBoxMed")]/text()')
		l.add_xpath('group','//h2[contains(.,"Part of the Following Group")]/following-sibling::ul[1]/li/a/text()')
		l.add_xpath('description', '//text()[	preceding::h2[.="Description"]	]')
		l.add_value('source','Mobygames')
		l.load_item() 
				
		logging.debug("Game Page parsed:" + item['title'])
		request = scrapy.Request("http://mobygames.com" + item['url'] + "/release-info",
			callback=self.parse_release)
		request.meta['item'] = item
		return request
		
		
		
	def parse_release(self, response):
	
		item = response.meta['item'] 
		
		title = item['search_title']
		region = item['search_region']
		
		logging.debug('Parsing ' + title + ' release data.')

		l = MobyLoader(item, response=response) 
		if region == 'EUR':
			xp = '//div[contains(@class,"relInfoDetails")]//span[' + \
			'contains(.,"United Kingdom") or ' + \
			'contains(.,"France") or ' + \
			'contains(.,"Italy") or ' + \
			'contains(.,"Germany") or ' + \
			'contains(.,"Worldwide")]/../../'
		elif region == 'USA':
			xp = '//div[contains(@class,"relInfoDetails")]//span[' + \
				'contains(.,"United States") or ' + \
				'contains(.,"Worldwide")]/../../' 
		elif region == 'JPN':
			xp = '//div[contains(@class,"relInfoDetails")]//span[' + \
				'contains(.,"Japan") or ' + \
				'contains(.,"Worldwide")]/../../'
		elif region == 'KOR':
			xp = '//div[contains(@class,"relInfoDetails")]//span['+ \
				'contains(.,"Korea")]/../../'
		elif region == 'BRA':
			xp = '//div[contains(@class,"relInfoDetails")]//span['+ \
				'contains(.,"Brazil")]/../../'
		elif region == 'CHN':
			xp = '//div[contains(@class,"relInfoDetails")]//span['+ \
				'contains(.,"China") or ' + \
				'contains(.,"Taiwan")]/../../'
		else:
			logging.warning('No region found:' + title + ":" + region)
			xp = '//div[contains(@class,"relInfoDetails")]//span/../../'

		l.add_value('region',region)
		l.add_xpath('date',xp + 'following-sibling::div[1]/div[contains(@class,"relInfoDetails")]/text()')					
		l.add_xpath('publisher',xp + '../preceding-sibling::div[contains(.,"Published by")][1]/a/text()')					
		l.add_xpath('developer',xp + '../preceding-sibling::div[contains(.,"Developed by")][1]/a/text()')					
		l.load_item() 
		
		logging.debug("Release Info parsed:" + item['title'])
		
		request = scrapy.Request("http://mobygames.com" + item['url'] + "/rating-systems",
			callback=self.parse_ratings)
		request.meta['item'] = item
			
		return request
			
			
			
	def parse_ratings(self, response):

		item = response.meta['item'] 
	
		logging.debug('Parsing ' + item['title'] + ' ratings.')

		l = MobyLoader(item, response=response) 
		l.add_xpath('rating','//table[contains(@summary,"Rating Categories and Descriptors")][1]//tr/td[3]/a/text()')
		l.load_item() 
		logging.debug("Rating Systems parsed:" + item['title'])
		
		request = scrapy.Request("http://mobygames.com" + item['url'] + "/screenshots",
			callback=self.parse_screenshots)
		request.meta['item'] = item
		return request



	def parse_screenshots(self, response):

		item = response.meta['item'] 
	
		logging.debug('Parsing ' + item['title'] + ' screensots.')

		max = str(self.settings['MAX_SCREENSHOTS'])

		l = MobyLoader(item, response=response) 			
		l.add_xpath('screenshot_urls','//div[contains(@class,"thumbnail-image-wrapper")][position() <= ' + max + ']/a/@style')
		l.load_item() 
		
		logging.debug("Screenshots parsed:" + item['title'])
		
		request = scrapy.Request("http://mobygames.com" + item['url'] + "/cover-art",
		callback=self.parse_covers)
		request.meta['item'] = item
	
		return request
		



	def parse_covers(self, response):

		item = response.meta['item'] 
		region = item['region']
		
		logging.debug('Parsing ' + item['title'] + ' covers.')

		l = MobyLoader(item, response=response) 			

		selector = Selector(response) 
		regionElems = selector.xpath('//span[@style="white-space: nowrap"]')
		
		match = []
		matchall = ['unitedstates','canada','unitedkingdom','france','italy','germany','europe','worldwide','japan','china','korea']
		if region == 'USA':
			match = ['unitedstates','canada']
		elif region == 'JPN':
			match= ['japan','china']
		elif region == 'EUR':
			match = ['unitedkingdom','france','italy','germany','europe','worldwide']
		else:
			match = ['unitedkingdom','france','italy','germany','europe','worldwide','brazil','unitedstates','canada']
		
		# check if any country from the matchRegions is
		# found in any child of the country elements
		#		
		cover_urls = []
		found = False
		for r in regionElems:
			regionVal = str ( r.xpath('text()').extract_first() ).replace(" ","").lower()
			if regionVal in match:
				cover_urls =  r.xpath('../../../../following-sibling::div[@class="row"][1]//a/@style').extract()
				found = True
				break

		if not found:
			for r in regionElems:
				regionVal = str ( r.xpath('text()').extract_first() ).replace(" ","").lower()
				if regionVal in matchall:
					cover_urls =  r.xpath('../../../../following-sibling::div[@class="row"][1]//a/@style').extract()
					found = True
					break
			
		if 'screenshot_urls' in item.keys():		
			l.add_value('image_urls', item['screenshot_urls'] + cover_urls)
		else:
			l.add_value('image_urls', cover_urls)

		l.load_item() 

		logging.debug("Covers parsed:" + item['title'])
		logging.info('Done:' + item['title'] )
		
		self.items.append(item)
		return item

	# remove parentheses and text inside them
	def remove_parentheses(self,x):
		if '(' in x and ')' in x:
			x = re.sub('\(.*?\)','',x)
		return x
                            			                                                                        		


