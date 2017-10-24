import string

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

# removes copyright-in-circle symbol
#
def strip_copyright(x):
	return x.strip(u"\u00A9")

# replaces underscore symbols with space
#
def replace_underscore(x):	
	return string.replace(x, "_", " ")
	
# removes left and right whitespace
#
def strip(x):
	return x.strip()

# chops rightmost parentheses
#
def rchop_parentheses(x):
	if x.endswith('('):
		return x[:-1]
	else:
		return x
	
def filter_empty(x):
	return None if x == "" else x


# keep text inside parentheses, discard the rest	
#
def in_parentheses(x):
	return x[x.find("(")+1:x.find(")")]

def validate_year(x):
	if '?' in x:
		return None
	else:
		return x
		
def cpcpower_image(x):
	if "http://www.cpc-power.com/" not in x:
		return "http://www.cpc-power.com/" + x
	return x
	
class CpcpowerLoader(ItemLoader):

	default_input_processor = Identity()
	default_output_processor = Identity()
 
	title_out = TakeFirst()
	source_out = TakeFirst()
	platform_out = TakeFirst()
	region_out = TakeFirst()
	typeins_out = TakeFirst()
	players_out = Join(';')
	genre_out = TakeFirst()
	group_out = Join(';')
	criticScore_in = MapCompose(strip, filter_empty)
	year_out = MapCompose(validate_year)	
	publisher_in = MapCompose(strip_copyright, rchop_parentheses, replace_underscore, strip )
	publisher_out = TakeFirst()
	presentation_out = MapCompose(unicode.strip)
	perspective_out = MapCompose(unicode.strip)
	visual_out = MapCompose(unicode.strip)
	pacing_out = MapCompose(unicode.strip)
	gameplay_out = MapCompose(unicode.strip)

	image_urls_in = MapCompose(cpcpower_image)
    
	
