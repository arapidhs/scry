scry
====

Web scraping engines with Python and Scrapy

Implemented Engines
==================

Engine: Mobygames / cpcpower
---------------
Automatically crawl and download metadata from mobygames / cpc-power for a single platform
including images.

Quick Start
- cd /mobygames
- $ scrapy crawl mobygames -platform=snes

Engine: kickass
---------------
Automatically perform category / keyword searches at kickasstorrents.com 
and queue them for download with transmission bit torrent client.
Setup a cron job to completely automate torrent searching and downloading.

Quick Start
- git clone git@github.com:arapidhs/scry.git
- cd /kickass
- $ scrapy crawl kickass -a category=books -a keywords='python,java'
- Setup a cron job to keep scraping at intervals

Example that runs the spider every morning at 09:00

> 00 09 * * * export DISPLAY=:0.0 && cd ~/scry/kickass && \ 
/usr/local/bin/scrapy crawl kickass -a category=books \ 
-a keywords='python,java,sclala topics' >> ~/scrapy.log 2>&1

Email an hourly updated list of downloading torrents and search results via cronjob

> 0 */1 * * * cd ~/development/scrapy/kickass && ~/development/scrapy/kickass/mail.sh

Installing Scrapy
-----------------
- sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
- echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list
- sudo apt-get update && sudo apt-get install scrapy-0.24

Official installation instructions
http://doc.scrapy.org/en/latest/intro/install.html#intro-install-platform-notes


