import json
import subprocess
import time
import urllib2

from scrapy.http.request import Request

class TorrentPipeline(object):

	def process_item(self, item, spider):		
			print 'Downloading ' + item['title'][0]
			path = 'http:'+item['torrent'][0]					
			subprocess.call(['./curl_torrent.sh',path])
			time.sleep(10) # pause to prevent 502 eror and hammering
			return item