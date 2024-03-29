NZ_tides_csv_to_ical.
Convert NZ tides files from csv to iCalendar format. These can be loaded into any compatible calendar, including the default Android calendar app (which may need an importer) and Thunderbird.
The processing will add a blocked out event, by default 2 hours extra either side of high tide. This can be configured when the script is run - see below

Author: Robin Paulson, robin@bumblepuppy.org

https://github.com/robinpaulson/NZ_tides_csv_to_ical

csv files are published by Land Information New Zealand under a Creative Commons Licence and are freely distributable

They can be obtained from: https://www.linz.govt.nz/sea/tides/tide-predictions

The "icalendar" python module is a required dependency, it can be installed from `pip` and is often included in the default repositories of many UNIX-like operating systems. The other modules appear to be included in a standard Python 3 distribution, this may differ for your operating system.

To convert files, run:
```
python NZ_tides_csv_to_ical.py "tide_csv" "leeway"
```
where "tide_csv" is the appropriate csv file for your location,

and "leeway" is the time between the start of the event and high tide, also the time between high tide and the end of the event
(that is, the length of the event is equal to 2 x "leeway")

See the "example_screenshot_akl.png" file for a screenshot of a Thunderbird calendar with tides for Auckland. The events are 4 hours long, that is the "leeway" variable is set to 2.

Licence: GNU GPL v3+
