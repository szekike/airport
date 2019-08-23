Cloudant Airport database searcher
version 1.0.0

Prepare your environment

You will need a Linux operating system with Python 2.7. installed. It may run on Python 3, but since the code was not tested on version 3, it is not supported.
The following standard packages and their versions are needed to run the program:

•	argparse	1.4.0
•	certify	2019.6.16
•	chardet	3.0.4
•	idna	2.8
•	lucene-querybuilder	0.2
•	pip	19.2.2
•	requests	2.22.0
•	setuptools	41.2.0
•	urllib3	1.25.3
•	wheel	0.33.6
•	wsgiref	0.1.2

when the above requirements are met the program should be able to execute.
Running the program
The program requires 3 flags to be set, in order to run, otherwise it will  present you a similar error message on the output:
  
  airport [-h] -lon LONGITUDE -lat LATITUDE -dis DISTANCE
  airport: error: argument -lon/--longitude is required


If you curious about the flags you can run the help flag for more information.

  airport [-h] -lon LONGITUDE -lat LATITUDE -dis DISTANCE

  Search closest airports

  optional arguments:
    -h, --help            show this help message and exit
    -lon LONGITUDE, --longitude LONGITUDE
                          The longitude coordinate. (between -180 and 180)
    -lat LATITUDE, --latitude LATITUDE
                          The latitude coordinate. (between -90 and 90)
    -dis DISTANCE, --distance DISTANCE
                          The radius of the search from the given longitude and
                          latitude point. (positive number)

But the help lists the longitude, latitude, and distance flag as optional, and they are not. This looks like a bug in the argparse package help module.

So a good run would look like this:

  python airport.py -lon 10.4 -lat -23.7 -dis 7.2

As current geological coordination stands the longitude should be between -180 and 180, the latitude should be between -90 and 90.
The distance value should be a positive number since the negative distance from a point is kind of impossible.
Ignoring the above rules will result an error message e.g: Got error The longitude coordinate should between -180 and 180!

If everything is fine then the results should look something like this:

  Name: Swakopmund Airport, pos: (lat: -22.6619, lon: 14.5681), distance from user given point: 4.29542887498
  Name: Walvis Bay Airport, pos: (lat: -22.9799, lon: 14.6453), distance from user given point: 4.30593963032
  Name: Terrace Bay, pos: (lat: -19.9705556, lon: 13.0244444), distance from user given point: 4.56031401785
  Name: Sossusvlei, pos: (lat: -24.489444, lon: 15.815278), distance from user given point: 5.47251840074
  Name: Sossusvlei Desert Lodge Airstrip, pos: (lat: -24.802812, lon: 15.891713), distance from user given point: 5.60134858598
  Name: Luderitz Airport, pos: (lat: -26.6874, lon: 15.2429), distance from user given point: 5.69018797317
  Name: Eros Airport, pos: (lat: -22.6122, lon: 17.0804), distance from user given point: 6.76838629217
  Name: Okaukuejo Airport, pos: (lat: -19.1492, lon: 15.9119), distance from user given point: 7.14778442946
  Name: Windhoek Hosea Kutako International Airport , pos: (lat: -22.486667, lon: 17.4625), distance from user given point: 7.16596701213

If something will go wrong during the run an error message should appear.

Limitations:

  Airports in the database which do not have a name will not appear in the results.
  Heavy dependence on current database response structure.
  Argparse package help module displays incorrect optional flags.

Developer notes:
  I tried to integrate the cloudant python client, unfortunately the all of my connection attempts failed or timed out. After reconfiguring my network I was able to reach the server but it returned the following error:

    requests.exceptions.HTTPError: 500 Server Error: Internal Server Error for url: https://mikerhodes.cloudant.com/_session 

  Even though curl and HTTP requests are worked fine. So version 1.0.0, for now, uses HTTP requests.


