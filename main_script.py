
#urllib package is used for making HTTP requests and manipulating URL's
#JSON package is used for manipulating the data sent by the API.
#sqlite3 package is used for Database purposes.

import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3

#set your api-key. API key acts like a security key.
#serviceurl is the base url to which we are making the requests. This can be found in the Documentation.
api_key = 'BS--------------------Yt';
serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

#ssl ..This is for HTTPS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#set the connection to a database. 
conn = sqlite3.connect('address-location.sqlite');
cur = conn.cursor();
cur.execute('''CREATE TABLE Location (id INTEGER PRIMARY KEY AUTOINCREMENT,address TEXT, status TEXT, 
    latitude REAL, longitude REAL, url TEXT)''');

#open the file which has the addresses
fname = input('Enter file name.. from which addresses will be read-- ');
if(len(fname) < 1):
    fname = "addresses.txt"; #if no file is specified, use this file
fhandler = open(fname);

for line in fhandler:
    print(line);
    cur.execute('SELECT * from Location where address = ?', (line,));
    row = cur.fetchone();
    if row is not None:
        continue;

    print("retreiving");
    #create a dictionary
    params = dict();
    params['address'] = line;
    params['key'] = api_key;
    url = serviceurl + urllib.parse.urlencode(params);

    data = urllib.request.urlopen(url,context = ctx);
    data = data.read().decode();

    data = json.loads(data);

    if (data["status"] == 'OK'):
        status = data["status"];
        lat = data["results"][0]["geometry"]["location"]["lat"];
        lng = data["results"][0]["geometry"]["location"]["lng"];
        cur.execute('''INSERT INTO Location(address,status,latitude,longitude,url) VALUES(?,?,?,?,?)''',
            (line,status,lat,lng,url,));

    conn.commit();

cur.close();
