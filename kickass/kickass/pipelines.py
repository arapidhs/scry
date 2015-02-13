import json
import os
import subprocess
import time
import urllib2

from scrapy.http.request import Request

class TorrentPipeline(object):

	def __init__(self):		
		if not os.path.exists('torrents'):
			os.makedirs('torrents')					

	def process_item(self, item, spider):		
		if not self.exists(item['title'][0]):
			self.download_item(item)
			time.sleep(5) # pause to prevent 502 eror and hammering
		return item

	def download_item(self, item):
		title = item['title'][0]
		print 'Downloading ' + title
		f = open('torrents/torrents.log', 'a')
		f.write(title+"\n")		
		f.close()
		path = item['torrent'][0]
		subprocess.call(['./curl_torrent.sh',path])

	def exists(self, title):
		for line in open('torrents/torrents.log','a+'):
			if title in line:
				return True
		return False
