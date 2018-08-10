import datetime
import os
from urllib.request import Request, urlopen

filename = "<year>-0<month>-0<day>-<hour>.json.gz"

today = datetime.datetime.today()
filename = filename.replace("<year>" , str(today.year))
filename = filename.replace("<month>", str(today.month))
filename = filename.replace("<day>"  , str(today.day))
filename = filename.replace("<hour>" , "0")#"{0..23}") #today.hour

url = "http://data.gharchive.org/" + filename
outputDirectory = "files"

print("Retrieving file: ")
print(filename)
print(" from url: ")
print(url)

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
