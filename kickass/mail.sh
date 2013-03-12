#!/bin/bash -l
# Send an email using ssmtp # of the cronjob results.
# The location of the log file is set at the cronjob entries
# The script assumes that is located at ~/scrapy.log

grep "Downloading" ~/scrapy.log | sort | uniq -u > mail.tmp
sed -i '1iSubject:Crontab Scry' mail.tmp
ssmtp username@youremail.com < mail.tmp
rm mail.tmp



