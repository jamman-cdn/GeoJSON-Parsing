This Python script fetches the given GeoJSON URL using command line arguments. The first argument is the URL to the file. The other command line argument is the number of days we want to go back. The reference coordinates have been hardcoded but can also be passed as arguments.

So the usage of this program is like - 
#python geojson.py http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson 7

The output will be -
The maximum intensity of the earthquake occured within 100 miles of Menlo Park office is 2.96 and is at 11km ENE of Yountville, California on 2015-01-29 19:04:41

The entire program depends on two important comparisions - 
1) Comparision between the coordinates and determining if the distance between them is less than 100 miles
2) Comparing the time stamp of the earth quake and the current time stamp and ensure that we are recording maximums only from those quakes that fall under the last 7 days.

Calculating distance between the coordinates:

For very accurate computations, we can use various APIs to compute the distance between the two coordinates. However, for the sake of this computation (just a 100 mile radius), we can safely assume that the earth is a perfect sphere and proceed accordingly to compute the arc length. Then multiplying it with 3960 gives us the number of miles.

Checking the timestamp:

The timestamp in the JSON file is in the form of epoch time with milliseconds included. I need to find out the date that is 7 days ago from now and convert that into epoch time. I then need to compare the time stamp of the earth quake with the epoch timestamp at this moment 7 days ago. If earth quake time stamp is more than the computed 7 days ago timestamp, then that earth quake becomes an eligible candidate.

Keeping track of the maximum:

I declared 3 variables - maximu, max_location, max_datetime that always keep track of the current max values. They update as we iterate through the list of earth quake occurances.

We finally arrive at one set of values that are maximum for a given number of days in the past within a 100 mile radius of Menlo Park office.