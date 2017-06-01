import sys
import scrapy
import logging

from scrapy.spiders import Spider
from scrapy.selector import Selector

class CpcPowerSpider(Spider):

	name = "cpcpower"
	
	def start_requests(self):
		# set default encoding to utf8 for parsing and logging
		# utf-8 characters in console and files
        #
		reload(sys)
		sys.setdefaultencoding('utf8')
		
		urls = [
			'http://www.cpc-power.com/index.php?page=detail&num=1396',
			'http://www.cpc-power.com/index.php?page=detail&num=1397',
			'http://www.cpc-power.com/index.php?page=detail&num=1398',
			'http://www.cpc-power.com/index.php?page=detail&num=1399',
			'http://www.cpc-power.com/index.php?page=detail&num=6992',
			'http://www.cpc-power.com/index.php?page=detail&num=2'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
			
	def parse(self, response):
	
		self.crawler.stats.inc_value('games_crawled')
		
		logging.debug('cpc-power reponse')
		logging.debug('Raw Response:' + response.body)
		
		selector = Selector(response)
		
		# Title xpath
		# //*[@id="cartouche_alias"]
		logging.info('\n')
		logging.info("Title:" + selector.xpath( '//*[@id="cartouche_alias"]/text()[1]' ).extract_first() )
		logging.info("Publisher:" + selector.xpath( '//*[@id="cartouche_titre"]/text()' ).extract_first() )
		logging.info("Year:" + selector.xpath( '//*[@id="cartouche_titre"]/a/span/text()' ).extract_first() )
		logging.info("Genre:" + selector.xpath( '//*[@id="cartouche_categorie"]/a/img/@alt' ).extract_first() )
		
