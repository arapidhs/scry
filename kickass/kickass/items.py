from scrapy.item import Item, Field

class TorrentItem(Item):
	title = Field()	
	url = Field()
	size = Field()
	sizeType = Field()
	age = Field()
	seed = Field()
	leech = Field()
	torrent = Field()

