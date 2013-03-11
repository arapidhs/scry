scry
====

Web scraping engines with Python and Scrapy

Implemented Engines
==================

Engine: kickass
---------------
Automatically perform category / keyword searches at kickasstorrents.com 
and queue them for download with transmission bit torrent client.
Setup a cron job to completely automate torrent searching and downloading.

Quick Start
-----------
- git clone git@github.com:arapidhs/scry.git
- cd /kickass
- $ scrapy crawl kickass -a category=books -a keywords='python,java'
- Setup a cron job to keep scraping at intervals

Example that runs the spider every morning at 09:00

> 00 09 * * * export DISPLAY=:0.0 && cd ~/scry/kickass && \ 
/usr/local/bin/scrapy crawl kickass -a category=books \ 
-a keywords='python,java,sclala topics' >> ~/scrapy.log 2>&1
