import logging
import os
import re
import sys

import xml.etree.ElementTree as ET

from collections import defaultdict

from platforms import Platforms

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor

from spiders.mobygames_spider import MobygamesSpider

class ParentClone:

	global platforms
	platforms = Platforms()
        
	def __init__(self, datpath=None):

		self.datpath = datpath
		
		if datpath:
        
        	# parse the xml dat file
        	#
			self.gamestree =  ET.parse(self.datpath).getroot()
			
			# identify platform
			#
			if self.gamestree.find('.//platform') is None:
				logging.error('No platform element found!')
				logging.error('Add a <platform/> xml element in the dat file.')
				logging.error('e.g.	<header>..<platform>Genesis</platform/>..</header>')
				return
			else:
				self.platform =  self.gamestree.find('.//platform').text
				logging.info('Platform:' + self.platform)
			
			if platforms.getId(self.platform) is None:
				logging.error('Platform ' + self.platform + ' not supported.')
				return
				
			# strip whitespace and remove text within parenetheses
			# from game names.
			# load adictionary with game name as key and a list 
			# of the regions it released
			#
			# e.g. the folloging xml entry
			#
			# <game name="NBA Live 95 (USA, Europe)">
			#     <description>NBA Live 95 (USA, Europe)</description>
			#     <release name="NBA Live 95 (USA, Europe)" region="EUR"/>
			#     <release name="NBA Live 95 (USA, Europe)" region="USA"/>
			#     <rom name="NBA Live 95 (USA, Europe).md" size="2097152" crc="66018ABC" /> 
			# </game>
			#
			# is loaded in the games{} dictionary as:
			# {'NBA Live 95': ['EUR', 'USA']}
			#
			self.games = defaultdict(list)
			
			for g in self.gamestree.findall('game'):
				if not g.attrib.get('cloneof'):
					name = self.normalizeName(g.attrib.get('name'))
					for r in g.findall('release'):
						self.games[name].append( r.attrib.get('region') )


			process = CrawlerProcess(get_project_settings())
			process.crawl('mobygames', url='http://mobygames.com/search/quick?q=air diver&p=16&search=Go&sFilter=1&sG=on')			
			process.crawl('mobygames', url='http://mobygames.com/search/quick?q=sonic r&p=16&search=Go&sFilter=1&sG=on')			
#			process.crawl(MobygamesSpider(url='http://mobygames.com/search/quick?q=air diver&p=16&search=Go&sFilter=1&sG=on'))
			process.start()						
			# init env. configuration and runner
			# 
			#configure_logging()
			#get_project_settings()
			#runner = CrawlerRunner()												
		
			#runner.crawl(MobygamesSpider(title='air diver',platform='genesis', region='EUR'))

			#d = runner.join()
			#d.addBoth(lambda _: reactor.stop())			

			# the script will block here until all 
			# crawling jobs are finished
			# 
			#reactor.run()			
			
		else:
			logging.warning('No dat file.')		
			
	# strip all text in parentheses
	#
	def normalizeName(self,value):
		value = re.sub(r'\([^)]*\)', '',  value )
		return value.strip()
                        			


