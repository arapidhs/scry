import logging
import math
import os
import re
import sys
import urllib
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from scrapy.utils.project import get_project_settings

from platforms import Platforms

from twisted.internet import reactor

from spiders.mobygames_spider import MobygamesSpider

class Importer:

	global platforms
	platforms = Platforms()
        
	def __init__(self, datpath=None, boxpath=None):

		logging.basicConfig(
			filename='import.log',
			filemode = 'a',
			format='%(levelname)s: %(message)s',
			level=logging.DEBUG
		)

		settings = get_project_settings()                
		imgpath = settings['IMAGES_STORE']
		
		# paths of source and target file
		# source file is the exported one from the exporter.py
		# target file is LaunchBox.xml metadata file
		self.datpath = datpath
		self.boxpath = boxpath	
		
		# counters for found and not found games
		self.inc_found = 0		
		self.inc_notfound = 0
		
		# store titles of not found games
		self.notfound = []
		
		if datpath and boxpath:
							
			self.dattree =  ET.parse(self.datpath)
			self.dat = self.dattree.getroot()
										
			if self.dat.find('.//platform[1]') is None:
				logging.error('No platform element found!')
				logging.error('Add a <platform/> xml element in the dat file.')
				logging.error('e.g. <platform>Genesis</platform/>')
				return
			else:
				self.platform =  self.dat.find('.//platform/[1]').text
				self.platform = platforms.getLaunchBoxPlatform(self.platform)
				self.imagesdir = self.boxpath + 'Images/' + self.platform + '/'
				self.frontdir = self.imagesdir + 'Box - Front/'
				self.backdir = self.imagesdir + 'Box - Back/'
				self.screenshotdir = self.imagesdir + 'Screenshot - Gameplay/Snap/'
				self.mediadir = self.imagesdir + 'Media/'
				
				if not os.path.exists(self.frontdir):
					os.makedirs(self.frontdir)				
				if not os.path.exists(self.backdir):
					os.makedirs(self.backdir)				
				if not os.path.exists(self.frontdir):
					os.makedirs(self.screenshotdir)				
				if not os.path.exists(self.screenshotdir):
					os.makedirs(self.screenshotdir)				
				if not os.path.exists(self.mediadir):
					os.makedirs(self.mediadir)				

				logging.info('Platform:' + self.platform)
				logging.info('Images destination directory:' + self.imagesdir)
	                                                                      
			# backup LaunchBox Data file
			#		
			if self.boxpath:
				boxfile = self.boxpath + 'Data/Platforms/' + self.platform + '.xml'
				shutil.copyfile(boxfile, boxfile + '.bak')	
				logging.info('Data directory:' + self.boxpath)
				logging.info('Data file:' + boxfile)
				logging.info('Data backup file:' + boxfile + '.bak')
				
			# Parse LaunchBox games for Platform
			#
			self.boxtree =  ET.parse(boxfile)
			self.box = self.boxtree.getroot()
		                                                                                                                        
			# load game elements into dicts
			# with key == title, value game elemtn
			_datgames = self.dat.findall('game')
			_boxgames = self.box.findall('Game')
			self.datgames = defaultdict(list)
			self.boxgames = defaultdict(list)
			
			# load all games in the dat file in dictionary
			# by title
			#
			for g in _datgames:
				title = g.find('./title').text
				title = self.remove_prefix(title,"The ")
				title = self.remove_suffix(title,", The")
				title = self.remove_suffix(title,"The")
				title = self.normalizeName(title)
				title = filter(str.isalnum, title.encode('utf-8')).lower().strip()
				self.datgames[title] = g
			totalgames = len(self.datgames)	
			
			# load all launchbox games for the given platform
			# and that exist in the dat file
			#
			for g in _boxgames:
				if g.find('Platform').text == self.platform:
					title = g.find('./Title').text
					title = self.remove_prefix(title,"The ")
					title = self.remove_suffix(title,", The")
					title = self.remove_suffix(title,"The")
					title = self.normalizeName(title)
					title = filter(str.isalnum, title.encode('utf-8')).lower().strip()
					self.boxgames[title] = g
						
			# delete keys from dat games that do not
			# have a match in launchbox
			#
			delkeys = []
			for key in self.datgames:
				if key not in self.boxgames.keys():
					delkeys.append(key)
					self.notfound.append(self.datgames[key].find('./title').text)
					self.inc_notfound += 1
				else:
					self.inc_found += 1
			for key in delkeys:
				del self.datgames[key]
				
				 
			logging.info('Importing ' + str(self.inc_found) +'/' + str(totalgames) + ' games.')
			logging.info('Not found games:' + str(self.inc_notfound))
			logging.info('List of not found games:' + str(self.notfound))

			chars_to_remove = ['\\', '/', ':', '?', '\'', '"']
			rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
			
			# Start the import
			#
			for key in self.datgames:
				logging.debug('Importing ' + self.datgames[key].find('./title').text )
				self.copyTag(key,'developer','Developer')
				self.copyTag(key,'publisher','Publisher')
				self.copyTag(key,'date','ReleaseDate')
				self.copyTag(key,'description','Notes')
				self.copyTag(key,'region','Region')
				self.copyTag(key,'source','Source')
				self.copyTag(key,'genre','Genre')
				self.copyTag(key,'group','Series')
				self.copyTag(key,'rating','Rating')
				
				gameId = self.boxgames[key].find('./ID').text
				
				# presentation custom field
				presentation = self.datgames[key].findall('./presentation//value')
				if len(presentation) > 0:
					for p in presentation:
						self.addCustomField(gameId,'Presentation',p.text)
						
				# perspective custom field
				perspective = self.datgames[key].findall('./perspective//value')
				if len(perspective) > 0:
					for p in perspective:
						self.addCustomField(gameId,'Perspective',p.text)
						
				# setting custom field
				setting = self.datgames[key].findall('./setting//value')
				if len(setting) > 0:
					for s in setting:
						self.addCustomField(gameId,'Setting',s.text)
						
				# pacing custom field
				pacing = self.datgames[key].findall('./pacing//value')
				if len(pacing) > 0:
					for p in pacing:
						self.addCustomField(gameId,'Pacing',p.text)

				# visual custom field
				visual = self.datgames[key].findall('./visual//value')
				if len(visual) > 0:
					for v in visual:					
						self.addCustomField(gameId,'Visual',v.text)
						
				# vehicular custom field
				vehicular = self.datgames[key].findall('./vehicular//value')
				if len(vehicular) > 0:
					for v in vehicular:
						self.addCustomField(gameId,'Vehicular',v.text)
						
				# gameplay custom field
				gameplay = self.datgames[key].findall('./gameplay//value')
				if len(gameplay) > 0:
					for g in gameplay:
						self.addCustomField(gameId,'Gameplay',g.text)
						
				# sport custom field
				sport = self.datgames[key].findall('./sport//value')
				if len(sport) > 0:
					for s in sport:
						self.addCustomField(gameId,'Sport',s.text)

				# exclusive custom field
				exclusive = self.datgames[key].findall('./exclusive')
				if len(exclusive) > 0:
					self.addCustomField(gameId,'Exclusive','Yes')
					
				# mature custom field
				mature = self.datgames[key].findall('./mature')
				if len(mature) > 0:
					self.addCustomField(gameId,'Mature','Yes')
				
				# licensed custom field
				licensed = self.datgames[key].findall('./licensed')
				if len(licensed) > 0:
					self.addCustomField(gameId,'Licensed Title','Yes')
				
				# user score -> star rating
				userRating = self.datgames[key].findall('./userScore/value')
				if len(userRating) > 0:
					userRating =int(math.ceil(float(userRating[0].text)))
					self.boxgames[key].find('./StarRating').text = str(userRating)
					
				# IMAGES
				images = self.datgames[key].findall('./images//value')
				screenshots = []
				media = []
				title = self.boxgames[key].find('./Title').text
				title = re.sub(rx, '_', title)
				for img in images:					
					url = img.find('./url').text
					path = imgpath +'/' +  img.find('./path').text					
					filename, file_extension = os.path.splitext(path)					
					if 'front-cover' in url:
						dest =  self.frontdir + title + file_extension
						shutil.copy(path,dest)
					elif 'back-cover' in url:
						dest =  self.backdir + title + file_extension
						shutil.copy(path,dest)
					elif 'screenshot' in url:
						screenshots.append(path)
					else:
						media.append(path)
						
				self.copyImages(title,media, self.mediadir)
				
				self.copyImages(title,screenshots, self.screenshotdir)
							
					
			self.boxtree.write(boxfile + '.import',encoding='utf-8')
			
		else:
			logging.warning('No dat and/or box file.')		
        

	# copies the text value inside a tag
    #
	def copyTag(self,key,source,target):
		game = self.datgames[key]
		_s = self.datgames[key].find('./' + source)
		if _s is not None:
			parent = self.boxgames[key]
			elem = parent.find('./' + target)
			if elem is not None:
				elem.text = _s.text
			else:
				elem = ET.SubElement(parent,target)
				elem.text = _s.text


	def addCustomField(self,gid,name,value):
		customfield = ET.SubElement(self.box,'CustomField')
		gidElem = ET.SubElement(customfield,'GameID')		
		gidElem.text = gid
		nameElem = ET.SubElement(customfield,'Name')
		nameElem.text = name
		valueElem = ET.SubElement(customfield,'Value')
		valueElem.text = value
	
	def copyImages(self,title,images,targetdir):
		if len(images) > 0:
			for idx, val in enumerate(images):						
				filename, file_extension = os.path.splitext(val)							
				if idx < 9:
					dest =  targetdir + title + '-0' + str(idx+1) + file_extension
				else:
					dest =  targetdir + title + '-' + str(idx+1) + file_extension
				shutil.copy(val,dest)
		    
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



	# remove prefix from text x
	def remove_prefix(self,x, prefix):
		if x.startswith(prefix):
			x = x[len(prefix):]
		return x



	# remove suffix from text x
	def remove_suffix(self,x, suffix):
		if x.endswith(suffix):
			x = x[:-len(suffix):]
		return x
		
