import logging
import dateutil.parser

from scrapy import signals
from scrapy.exporters import XmlItemExporter

class MobygamesPipeline(object):

	global adult_ratings
	adult_ratings = ['18', 'Adults Only']
	global licensed
	licensed = [u'Licensed\xa0Title']
	
	def __init__(self):
		self.files = {}
	
	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline
	  	 	 	 	 
	def spider_opened(self, spider):
		file = open(spider.settings['FILES_STORE'] + '/%s.xml' % 'export', 'w+b')
		self.files[spider] = file
		self.exporter = XmlItemExporter(file,item_element='game', root_element='games')
		self.exporter.start_exporting()
		return
  	 	 	 	 				
	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()
		return

	def process_item(self, item, spider):
		logging.info("Exporting item:" + item['title'])
		
		# do not export utility fields
		# pop them from item dict
		item.pop("search_region", None)
		item.pop("search_title", None)
		item.pop("search_platform", None)
		item.pop("screenshot_urls", None)
		item.pop("cover_urls", None)

		if 'date' in item.keys():
			item['date'] = str(dateutil.parser.parse(item['date']))
			
		if 'rating' in item.keys():
			if [i for i in adult_ratings if i in item['rating']]:
				item['mature'] = ''			
				item['rating'] = '18'
			else:
				item['rating'] = item['rating'][0]
		
		if 'misc' in item.keys():
			if [i for i in licensed  if i in item['misc']]:
				item['licensed'] = ''			
		
		try:
			value = item['platforms']
		except KeyError:
			# Key is not present
			item['exclusive'] =''
			pass		
            
		# clean up description				
		d = item['description'].encode('utf-8')
		start = 0
		end = d.find('[ edit description')
		item['description'] = d[start:end].strip().replace("  "," ")
		
		self.exporter.export_item(item)
		return item
