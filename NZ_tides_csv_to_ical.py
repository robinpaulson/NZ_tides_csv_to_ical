#!/usr/bin/python3

# This Python script will convert tide date from csv to iCal files.
# csv files are published by Land Information New Zealand
# They can be obtained from: http://www.linz.govt.nz/sea/tides/tide-predictions
# To convert: ./NZ_tides_csv_to_ical.py "tide_csv" "leeway"
# where "tide_csv" is the appropriate csv file for your location
# and "leeway" is the amount of time either side of high tide to block out for
# the calendar event

# Author: Robin Paulson, robin@bumblepuppy.org
# https://github.com/robinpaulson/NZ_tides_csv_to_ical
# Licence: GNU GPL 3+

# requires "icalendar" module, which is not part of a default Python install
# (on Ubuntu, anyway)

import calendar
import csv
import icalendar
import os
import pytz
import sys
import time
from datetime import datetime
from datetime import timedelta
from time import mktime

# the first three lines of the csv files are header, we ignore these
read_line=3

# add some info to the top of the .ics file to identify what it is for
# we should probably set this to something meaningful/useful/consistent
# with the ical format
# TODO: look up ical format for information on this
cal = icalendar.Calendar()
cal.add('prodid', '-//NZ high tides calendar//')
cal.add('version', '1.0')

# get the name of the csv file we are getting the data from
# TODO: add graceful error-handling in case the user does not specify a file
csv_file = sys.argv[1]

# amount of time either side of high tide to block out
# "2" will block out two hours before and two hours after
# by default, time is +/- 2 hours
# setting the second variable to a number will use that number instead

if len(sys.argv) < 3:
	leeway = 2
else:
	# TODO: print an error message and exit if the user specifies a leeway > 6
	leeway = int(sys.argv[2])

with open(csv_file, 'r') as csvfile:
	tide_reader = csv.reader(csvfile, delimiter=',')
	mycsv=list(tide_reader)
	tide_location=mycsv[0][1]
	tide_year=mycsv[read_line][3]
	if calendar.isleap(int(tide_year))==True:
		num_readlines=369
	else:
		num_readlines=368
	while (read_line < num_readlines):
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
				# We can read first and second entries, compare to find which is
				# highest, then read every other data point and create cal
				# entries
				if (float(tide_height) > 1.6):
					# TODO: can we add leading zeroes by using format codes?
					if (len(tide_month)==1):
						tide_month='0'+tide_month
					if (len(tide_date)==1):
						tide_date='0'+tide_date
					full_time = tide_year + tide_month + tide_date + tide_time
					ht_struct = time.strptime(full_time, '%Y%m%d%H:%M')
					desc_struct = time.strptime(tide_time, '%H:%M')
					# convert time from time to datetime formats
					ht_dt = datetime.fromtimestamp(mktime(ht_struct))
					desc_dt = datetime.fromtimestamp(mktime(desc_struct))
					# calculate the offsets for the start and end of the block
					block_start = ht_dt - timedelta(hours=leeway)
					block_end = ht_dt + timedelta(hours=leeway)
					event = icalendar.Event()
					# add the tide height to the "summary" field
					event.add('summary', tide_height + "  " + str(tide_time))
					# start and end of each block
					event.add('dtstart', block_start)
					event.add('dtend', block_end)
					event.add('dtstamp', ht_dt)
					# add the location to the event
					event.add('location',tide_location)
					cal.add_component(event)
			tide_num=tide_num+2
f = open(tide_location+'_'+tide_year+'.ics', 'wb')
f.write(cal.to_ical())
f.close()
