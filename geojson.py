import json
import math
import time
from datetime import datetime, timedelta, date
from sys import argv
import urllib2
 
def distance(ref_lat, ref_long, lat, longitude):
 
    # Converting degrees to radians
    d_to_r = math.pi/180.0
         
    # Calculating pi
    pi1 = (90.0 - ref_lat)*d_to_r
    pi2 = (90.0 - lat)*d_to_r
         
    # Calculating theta
    theta1 = ref_long*d_to_r
    theta2 = longitude*d_to_r
         
    # Computing spherical distance
     
    cos = (math.sin(pi1)*math.sin(pi2)*math.cos(theta1 - theta2) + 
           math.cos(pi1)*math.cos(pi2))
    arc = math.acos( cos )
 
    # Converting arc length to miles
    return 3960*arc

# Fetching the URL from command line
script, url, daysback = argv

# Some basic sanitation check
if url[:4] != "http":
    print "Please make sure the URL starts with either http:// or https:// and should be a valid GeoJSON URL"
    exit(1)

# Pulling data to fh
fh = urllib2.urlopen(url)

# Loading data into JSON decoder
data = json.load(fh)

# 7 Days ago, the date was delta
delta = date.today() - timedelta(days=int(daysback))

# Converting 7 days ago date to epoch time
pattern = '%Y-%m-%d'
epoch = int(time.mktime(time.strptime(str(delta), pattern)))

print epoch

# Calculating number of earth quakes in the json file
iterate = len(data['features'])

# Taking the Menlo Park office as the center of the calculation
ref_lat = 37.452278
ref_long = -122.166203

# Initiating the maximum to 0; we will update this as we parse through the JSON file
maximum = 0
max_location = ""
max_datetime = ""

for i in xrange(iterate):
    # Measuring if distance between the ref coordinates and the earth quake coordinates is less than 100 miles and also checking if time of occurance (in epoch) is greater than the epoch value of date 7 days ago, since we wanted this for one week
    if distance(ref_lat, ref_long, data['features'][i]['geometry']['coordinates'][1], data['features'][i]['geometry']['coordinates'][0]) < 100 and data['features'][i]['properties']['time']/1000 > float(epoch):
        # If the magnitude of current iteration earth quake is greater than the max of all previous earth quakes, we update the maximum variable with new record
        if(data['features'][i]['properties']['mag'] > maximum):
            maximum = data['features'][i]['properties']['mag']
            max_location = data['features'][i]['properties']['place']
            max_datetime = datetime.fromtimestamp(int(data['features'][i]['properties']['time']/1000)).strftime('%Y-%m-%d %H:%M:%S')

if maximum == 0:
    print "Hurray! There was no earth quake in the past 7 days in the 100 mile radius of our Menlo Park office."
else:
    # Printing the maximum intensity
    print "The maximum intensity of the earthquake occured within 100 miles of Menlo Park office is", maximum, "and is at", max_location, "on", max_datetime

fh.close()