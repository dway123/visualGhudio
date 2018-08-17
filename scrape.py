import datetime
from urllib.request import Request, urlopen

fileTitle = datetime.datetime.now().strftime("%Y-%m-%d-{0..23}")
fileExt = ".json.gz"
fileName = fileTitle + fileExt

url = "http://data.gharchive.org/" + fileName
outputDirectory = "files"

print("Retrieving file: ")
print(fileName)
print(" from url: ")
print(url)

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
