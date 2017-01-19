NZ_tides_csv_to_ical.
Convert NZ tides files from csv to iCal format. These can be loaded into any calendar, such as Android and Thunderbird.
The processing will add a blocked out event, by default 2 hours extra either side of high tide. This can be configured in the script by adjusting the "leeway" parameter.

Author: Robin Paulson, robin@bumblepuppy.org

https://github.com/robinpaulson/NZ_tides_csv_to_ical

csv files are published by Land Information New Zealand

They can be obtained from: http://www.linz.govt.nz/sea/tides/tide-predictions

The "icalendar" python module is a required dependency

To convert files, run:

python NZ_tides_csv_to_ical.py <tide_csv>

where <tide_csv> is the appropriate csv file for your location

Licence: GNU GPL 3+
