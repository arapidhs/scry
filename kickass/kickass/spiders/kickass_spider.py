from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.gz import gunzip

from kickass.items import TorrentItem

class KickassSpider(Spider):

	name = "kickass"

	allowed_domains = [
		"kat.ph"
	]

	def __init__(self, *args, **kwargs): 
		super(KickassSpider, self).__init__(*args, **kwargs)
		self.keywords = kwargs['keywords'].split(',')
		self.category = kwargs['category']
		self.start_urls = [
			'http://kickass.to/' 
			+ self.category 
			+ '/?field=time_add&sorder=desc'
		]

	def parse(self, response):
		selector = Selector(response)
		entries = selector.xpath('//tr[starts-with(@id,"torrent_")]')
		print(entries)
		items = []
		for entry in entries:
			item = TorrentItem()
			item['title'] = entry.xpath('td[1]/div[2]/div/a/text()').extract()
			print(item['title'])
			for s in self.keywords:
				if s.lower() in item['title'][0].lower():
					item['url'] = entry.select('td[1]/div[1]/a[3]/@href').extract()
					item['torrent'] = entry.select('td[1]/div[1]/a[starts-with(@title,"Download torrent file")]/@href').extract()
					item['size'] = entry.select('td[2]/text()[1]').extract()
					item['sizeType'] = entry.select('td[2]/span/text()').extract()
					item['age'] = entry.xpath('td[4]/text()').extract()
					item['seed'] = entry.select('td[5]/text()').extract()
					item['leech'] = entry.select('td[6]/text()').extract()					
					items.append(item)
					break			
		return items
		
