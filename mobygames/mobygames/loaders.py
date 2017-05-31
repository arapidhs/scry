from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

def strip_dots(x):
	return x.strip('.')    
	
	
def filter_empty(x):
	return None if x == "" else x


# keep text inside parentheses, discard the rest	
#
def in_parentheses(x):
	return x[x.find("(")+1:x.find(")")]


def moby_image(x):
	if '/images/shots/s'in x:
		return x.replace('/images/shots/s',	'http://mobygames.com/images/shots/l')
	else:
		return x.replace('/images/covers/s',	'http://mobygames.com/images/covers/l')

class MobyLoader(ItemLoader):

	default_input_processor = Identity()
	default_output_processor = Identity()
 
	title_out = TakeFirst()
	source_out = TakeFirst()
	platform_out = TakeFirst()
	region_out = TakeFirst()
	description_out = Join()
	genre_out = Join(';')
	group_out = Join(';')
	criticScore_in = MapCompose(strip_dots, filter_empty)
	userScore_in = MapCompose(strip_dots, filter_empty)
	date_out = TakeFirst()
	publisher_out = TakeFirst()
	developer_out = TakeFirst()
	presentation_out = MapCompose(unicode.strip)
	perspective_out = MapCompose(unicode.strip)
	visual_out = MapCompose(unicode.strip)
	vehicular_out = MapCompose(unicode.strip)
	pacing_out = MapCompose(unicode.strip)
	setting_out = MapCompose(unicode.strip)
	gameplay_out = MapCompose(unicode.strip)
	pacing_out = MapCompose(unicode.strip)

	image_urls_in = MapCompose(in_parentheses,moby_image)
    
	
