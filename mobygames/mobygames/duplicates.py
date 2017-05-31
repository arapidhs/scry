from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		if item['title'] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item['title'])
		else:
			self.ids_seen.add(item['title'])
		return item
