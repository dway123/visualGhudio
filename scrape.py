import datetime

import wget
import datetime
from wget import download
import os

fileExt = ".json.gz"

fileTitle = datetime.datetime.now().strftime("%Y-%m-%d-{0..23}")
fileName = fileTitle + fileExt

url = "http://data.gharchive.org/" + fileName
outputDirectory = "files"

print("Retrieving file: ")
print(fileName)
print(" from url: ")
print(url)

#filename = wget.download(url, out=outputDirectory)
urllib.urlretrieve(url, outputDirectory + "/" + fileName)
