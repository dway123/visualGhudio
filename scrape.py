from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import gzip
import json

# We look at 1 hour delayed data.
delayedTime = datetime.utcnow() - timedelta(hours=2)

# fileTitle, for example, should be 2018-08-15-2 for 2018/8/15 2AM.
# Month and day is zero padded but hour is not zero padded.
fileTitle = delayedTime.strftime("%Y-%m-%d-") + delayedTime.strftime("%H").replace('0', '', 1)
fileExt = ".json.gz"
fileName = fileTitle + fileExt

url = "http://data.gharchive.org/" + fileName
outputDirectory = "files"

print("Retrieving file: ")
print(fileName)
print(" from url: ")
print(url)

request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(request)

compressedFile = response.read()
decompressedFile = gzip.decompress(compressedFile)

#TODO: Interpret this data as a string! That should fix the JSON interpreting problems, as the data is't a valid file
print(type(decompressedFile))
data = decompressedFile.decode('utf-8').replace('\n', '')
print(type(data))

jsonData = json.loads(data)

print(jsonData["payload"]["pull_request"]["head"]["repo"]["languages_url"])
#print(decompressedFile)
