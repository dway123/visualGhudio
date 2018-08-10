import wget
import datetime
from wget import download
import os


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

#filename = wget.download(url, out=outputDirectory)
urllib.urlretrieve(url, outputDirectory + "/" + filename)
