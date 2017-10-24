import logging
import os
import re
import sys
import urllib

import xml.etree.ElementTree as ET
from collections import defaultdict

from platforms import Platforms

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor

from spiders.mobygames_spider import MobygamesSpider

# parsers a roms xml datfile, extracts titles and regions
# and sends the constructed urls to mobygames spider for scraping
class Exporter:

	global platforms
	platforms = Platforms()
        
	def __init__(self, datpath=None):

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
			
			platformId = platforms.getId(self.platform)			
			if platformId is None:
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
			self.romnames = defaultdict(list)
			urls = []
														
			for g in self.gamestree.findall('game'):
			
				if not g.attrib.get('cloneof'):
									
					# For Mame ( Arcade ) platform, read the name of the game
					# from <description> tag.
					# That is because MAME dat files, in the name attribute store
					# the romname instead of the game title.
					# This is an exception for the Arcade platform only.
					# 															
					if self.platform == 'Arcade':						
						name = self.normalizeName(g.find('./description').text)
					else:
						name = self.normalizeName(g.attrib.get('name'))					
					name = name.encode('utf-8')

					if not name in self.games.keys():
					
						romname = ''
						rom =  g.find('./rom/[1]')
						if rom != None:
							romname = rom.attrib.get('name')
						self.romnames[name].append( romname )
					
						releases = g.findall('release')
						if releases:
							for r in releases:
								self.games[name].append( r.attrib.get('region') )
						else:
							self.games[name].append( 'Worldwide')


			for g in self.games:
			
				logging.debug('Submitting title:' + g + ':' + str ( self.games[g][0] )  )
				
				urls.append(
					'http://mobygames.com/search/quick' +
					'?q=' + g +
					'&p=' + platformId +
					'&search=Go'
					'&sFilter=1'
					'&sG=on'
					'&search_title=' + urllib.quote(g) + 
					'&search_platform=' + urllib.quote(self.platform) +
					'&search_region=' + urllib.quote(self.games[g][0]) +
					'&romname=' + urllib.quote(self.romnames[g][0])
				)
				
			process = CrawlerProcess(get_project_settings())
			process.crawl(MobygamesSpider, start_urls=urls)
			process.start()						

		else:
		
			logging.warning('No dat file.')		
			
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
                                    		
                        			


