import logging
import sys
import scrapy
import urlparse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from cpcpower.items import CpcpowerItem
from cpcpower.loaders import CpcpowerLoader

class CpcpowerSpider(Spider):

	global link_game
	link_game = "http://www.cpc-power.com/index.php?page=detail&num="
	
	global link_package
	link_package = "http://www.cpc-power.com/index.php?page=detail&onglet=package&num="
	
	global link_goodies
	link_goodies = "http://www.cpc-power.com/index.php?page=detail&onglet=goodies&num="

	global link_publications
	link_publications = "http://www.cpc-power.com/index.php?page=detail&onglet=pub&num="
			
	# exlcude genres that contain:
	global itemfilter		
	itemfilter = [
		"DEMO", "UTILITY", "COMPILATION -> Unofficial",
		"COMPILATION -> Press", "UNRELEASED", "DiscMag",
		"Trainer", "Forecast", "OTHER -> CrackTro",
		"OTHER -> Forecast"
	]
	
	name = "cpcpower"
	items = []
		
	platform = "Amstrad CPC"
	region = "EUR"
	source = "cpc-power"
	
	def start_requests(self):
		# set default encoding to utf8 for parsing and logging
		# utf-8 characters in console and files
        #
		reload(sys)
		sys.setdefaultencoding('utf8')
			
		urls = [
			'http://www.cpc-power.com/index.php?page=detail&num=51'
		]
		
		#~ urls = []
		#~ maxnum = 14387				
		#~ for i in range( maxnum ):
			#~ urls.append( link_game + str( i+1 ) )							
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	# parses main game page information
	#
	def parse(self, response):
	
		self.crawler.stats.inc_value('games_crawled')
		
		logging.debug('cpc-power reponse')		
		
		selector = Selector(response)
		
		# check if genre is DEMO and exclude it
		# else continue parsing
		genre = selector.xpath( '//*[@id="cartouche_categorie"]/a/img/@alt' ).extract_first()
		
		if any( flt in genre for flt in itemfilter ):		
			self.crawler.stats.inc_value('demo')
			return
		else:		
			self.crawler.stats.inc_value('games')
			
			item = CpcpowerItem()

			# parse num parameter from response url
			parsed = urlparse.urlparse(response.url)
			search_params = urlparse.parse_qs(parsed.query)
			search_num = search_params['num'][0]

			# load the item
			loader = CpcpowerLoader(item, response=response)
			loader.add_xpath( 'typeins', '//*[@id="cartouche_categorie"]/img[@alt="typeins"]' )
			loader.add_xpath( 'title', '//*[@id="cartouche_alias"]/text()[1]' )
			loader.add_xpath( 'publisher', '//*[@id="cartouche_titre"]/text()[1]' )
			loader.add_xpath( 'year', '//*[@id="cartouche_titre"]/a/span/text()' )
			loader.add_xpath( 'group', '//h2[.="Keywords"]/following-sibling::div[1]/a/text()' )
			loader.add_xpath( 'genre', '//div[.="- CATEGORIES -"]/following-sibling::div[1]/a/text()' )
			loader.add_xpath( 'players', '//div[.="- NUMBER OF PLAYERS -"]/following-sibling::div[1]//text()' )
			loader.add_xpath( 'criticScore', '//*[@id="evaluation"]/text()')
			loader.add_xpath( 'screenshot_urls', '//div[contains(@class,"decordiapo")]/img[contains(@alt,"screenshot")]/@src')
			loader.add_value( 'source', self.source)
			loader.add_value( 'region', self.region)
			loader.add_value( 'platform', self.platform)			
			loader.add_value( 'search_num', search_num )
			loader.load_item()
			
			# prepare and send request to parse 
			# packaging images ( covers, discs )
			# 
			request = scrapy.Request(link_package + item['search_num'][0],callback=self.parse_package)
			request.meta['item'] = item
			return request
		
	# parses packaging page, covers, tapes, discs
	#
	def parse_package(self, response):
		item = response.meta['item']
		
		# parse package urls, covers and discs
		#
		selector = Selector(response)		
		package_urls = selector.xpath( '//div[contains(@class,"picturesextra")]/a/img/@src').extract()
		
		# load screenshot and package urls to one item key
		# named image_urls		
		#
		loader = CpcpowerLoader(item, response=response)
		if 'screenshot_urls' in item.keys():
			loader.add_value('image_urls', item['screenshot_urls'] + package_urls)
		else:
			loader.add_value('image_urls', package_urls)
		loader.load_item()
		
		# prepare and send request to parse 
		# goodies images
		# 
		request = scrapy.Request(link_goodies + item['search_num'][0],callback=self.parse_goodies)
		request.meta['item'] = item
		return request
		
	# parses goodies images and adds them to image_urls key
	#	
	def parse_goodies(self, response):
		item = response.meta['item']

		# parse goodies urls
		#
		selector = Selector(response)		
		goodies_urls = selector.xpath( '//div[contains(@class,"picturesextra")]/a/img/@src').extract()
		
		loader = CpcpowerLoader(item, response=response)
		if 'image_urls' in item.keys():
			tmpimages = list( item['image_urls'] )			
			loader.add_value('image_urls', tmpimages + goodies_urls)
		else:
			loader.add_value('image_urls', goodies_urls)
		loader.load_item()

		# prepare and send request to parse 
		# goodies images
		# 
		request = scrapy.Request(link_publications + item['search_num'][0],callback=self.parse_publications)
		request.meta['item'] = item
		return request
		
	# parses publication images and adds them to image_urls key
	#	
	def parse_publications(self, response):
		item = response.meta['item']

		# parse publication urls
		#
		selector = Selector(response)		
		publication_urls = selector.xpath( '//div[contains(@class,"picturesextra")]/a/img/@src').extract()
		
		loader = CpcpowerLoader(item, response=response)
		if 'image_urls' in item.keys():
			tmpimages = list( item['image_urls'] )			
			loader.add_value('image_urls', tmpimages + publication_urls)
		else:
			loader.add_value('image_urls', publication_urls)
		loader.load_item()
		
		self.items.append(item)
		return item		
		
