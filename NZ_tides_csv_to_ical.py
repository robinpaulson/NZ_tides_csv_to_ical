#!/usr/bin/python

# This Python script will convert tide date from csv to iCal files.
# csv files are published by Land Information New Zealand
# They can be obtained from: http://www.linz.govt.nz/sea/tides/tide-predictions
# To convert: ./NZ_tides_csv_to_ical.py <tide_csv>
# where <tide_csv> is the appropriate csv file for your location
# Author: Robin Paulson, robin@bumblepuppy.org
# https://github.com/robinpaulson/NZ_tides_csv_to_ical
# Licence: GNU GPL 3+


import csv
import icalendar
import os
import pytz
import sys
import time
from datetime import datetime
from datetime import timedelta
from time import mktime

leeway=2

# the first two lines of the csv files are header, we ignore these
read_line=3

cal = icalendar.Calendar()
cal.add('prodid', '-//NZ high tides calendar//')
cal.add('version', '1.0')

# get the name of the csv file we are getting the data from
csv_file = sys.argv[1]

# amount of time either side of high tide to block out
# "2" will block out two hours before and two hours after
# by default, time is +/- 2 hours
# setting the second variable to a number will use that number instead
if sys.argv[2] == "":
	leeway = 2
else:
	leeway = int(sys.argv[2])

print leeway

# figure out the location name from the file name
tide_location=sys.argv[1].split('_')[0]

with open(csv_file, 'rb') as csvfile:
	tide_reader = csv.reader(csvfile, delimiter=',')
	mycsv=list(tide_reader)
#number of lines is hardcoded in. TODO: figure out how to do this dynamically
	while (read_line < 368):
		tide_year=mycsv[read_line][3]
		tide_month=mycsv[read_line][2]
		tide_date=mycsv[read_line][0]
		read_line=read_line+1
		tide_num=0
		while (tide_num < 8):
			tide_time=mycsv[read_line-1][tide_num+4]
			tide_height=mycsv[read_line-1][tide_num+5]
			# discard "empty" tides, for days with only three tide events
			if len(tide_height) > 0:
				# is the tide a high or low? TODO: find better ways to do this
				# in Auckland, 1.6m is half way between max low and min high
				if (float(tide_height) > 1.6):
					if (len(tide_month)==1):
						tide_month='0'+tide_month
					if (len(tide_date)==1):
						tide_date='0'+tide_date
					full_time = tide_year + tide_month + tide_date + tide_time
					ht_struct = time.strptime(full_time, '%Y%m%d%H:%M')
					# convert time from time to datetime formats
					ht_dt = datetime.fromtimestamp(mktime(ht_struct))
					# calculate the offsets for the start and end of the block
					block_start = ht_dt - timedelta(hours=leeway)
					block_end = ht_dt + timedelta(hours=leeway)
					event = icalendar.Event()
					# add the tide height to the "summary" field
					event.add('summary', tide_height)
					# start and end of each block
					event.add('dtstart', block_start)
					event.add('dtend', block_end)
					event.add('dtstamp', ht_dt)
					# add the location field to the event
					event.add('location',tide_location + ', New Zealand')
					cal.add_component(event)
			tide_num=tide_num+2
f = open(tide_location+'_'+tide_year+'.ics', 'wb')
f.write(cal.to_ical())
f.close()
