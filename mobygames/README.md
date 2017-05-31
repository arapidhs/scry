# crawl command for a single game
scrapy crawl mobygames -a title='air diver' -a platform='genesis' -a region='EUR'

# run spider from cli/bash
scrapy runspider ~/dev/src/scry/mobygames/mobygames/spiders/mobygames_spider.py -a title="air diver" -a platform="16" -a region="EUR"

# python script to scrap and export a parent/clone dat file
# notice that the dat file should include a <platform/> element with the name of the platform
#
# export.xml and images are downloaded under files directoy, 
# configured in settings.py
# see FILES_STORE, IMAGES_STORE
from mobygames.spiders.mobygames_spider import MobygamesSpider
from mobygames.items import MobygamesItem
from mobygames.exporter import Exporter

s = Exporter('path-to-datfile-xml')

# pretty print json
cat export.json | python -m json.tool

# pretty print xml
xmllint --format export.xml

# grep log for info OR[\|] warning log messages
grep -i 'INFO\|WARNING' mobygames.log
