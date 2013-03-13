#!/bin/bash -l
# Send an email using ssmtp # of the cronjob results.

FILE='torrents/torrents.log'

cp $FILE mail.tmp
sed -i '1iSubject:Crontab Scry' mail.tmp
ssmtp username@mail.com < mail.tmp
rm mail.tmp
