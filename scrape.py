from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import gzip
import json


def get_file_title_with_date(target_date) :
    return target_date.strftime("%Y-%m-%d-") + target_date.strftime("%H").replace('0', '', 1)


def get_url(prefix, file_title, extension=None) :
    return_url = prefix + file_title

    if extension is not None:
        return_url += ('.' + extension)

    return return_url


def get_response(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(request)

    return response.read()


def get_languages_url_from_json(json_data):
    return json_data["payload"]["pull_request"]["head"]["repo"]["languages_url"]


# We look at 1 hour delayed data.
delayed_time = datetime.utcnow() - timedelta(hours=2)
title = get_file_title_with_date(delayed_time)
url = get_url("http://data.gharchive.org/", title, "json.gz")
response = get_response(url)
data_file = gzip.decompress(response)
data_list = data_file.decode('utf-8').split('\n')
print(get_languages_url_from_json(json.loads(data_list[0])))