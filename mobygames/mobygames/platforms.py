import os
import re
import xml.etree.ElementTree as ET

from collections import defaultdict


class Platforms:

	global script_dir
	script_dir = os.path.dirname(__file__)

	platforms = {}
	platforms = defaultdict(list)
	launchbox_platforms = {}
	launchbox_platforms = defaultdict(list)


	# load 'platforms.xml' to a dictionary	
	# e.g. {.. 'atari st': '24', .. }
	#
	def __init__(self):
		self.platformpath = os.path.join(script_dir, "platforms.xml")
		self.root =  ET.parse(self.platformpath).getroot()
		for p in self.root.findall('./option'):
			self.platforms[p.text.lower()]=p.get('value')
			if 'launchbox' in p.keys():
				self.launchbox_platforms[p.text.lower()]=p.get('launchbox')

	def getId(self,value):
		return self.platforms.get(value.lower())
		
	def getLaunchBoxPlatform(self,value):
		return self.launchbox_platforms.get(value.lower())

	# strip text in parentheses
	#
	def normalizeName(self,value):
		value = re.sub(r'\([^)]*\)', '',  value )
		return value.strip()
