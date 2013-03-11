Kickass Spider
================

The kickass spider scraps latest torrents for a given category from kickasstorrents.com per 
and matches them to a keyword list.

The KickassSpider simply inherits Scrapy's framework BaseSpider and accepts two arguments:
- category = the category of kickass torrents e.g books,comics etc
- keywords = comma separated list of keywords to search for

How To
------
- git clone git@github.com:arapidhs/scry.git
- cd <project dir>/kickass
- $ scrapy crawl kickass -a category=books -a keywords='python,java'
- Setup a cron job to keep scraping at intervals

Prerequisites
-------------
Python and Scrapy framework

- sudo apt-get install python - Python 2.6 or 2.7
- Prerequisities for Scrapy
- sudo apt-get install python-dev - python dev libraries
- sudo apt-get install libxml2
- pip install Scrapy or easy_install Scrapy - Scrapy framework


Usage
-----
- Navigate within the project's directory e.g. kickass and run scrapy, for example:
- scrapy crawl kickass -a category=books -a keywords='python,java,sclala topics'

Setup a cron job to have the spider run at intervals:

From the command line type
crontab -e
and add the following line to run the spider every 20 minutes

> */20 * * * * cd ~/scry/kickass && \ 
/usr/local/bin/scrapy crawl kickass -a category=books \ 
-a keywords='python,java,sclala topics' >> ~/scrapy.log 2>&1

Another example that runs every morning at 09:00

> 00 09 * * * cd ~/scry/kickass && \ 
/usr/local/bin/scrapy crawl kickass -a category=books \ 
-a keywords='python,java,sclala topics' >> ~/scrapy.log 2>&1


