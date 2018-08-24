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
    try:
        return json_data["payload"]["pull_request"]["head"]["repo"]["languages_url"]
    except KeyError:
        #print("KeyError")
        return None
    except TypeError:
        print("TypeError")
        print("json_data is " + str(json_data) if json_data is not None else "None")
        return None
    except:
        print("Some generic error")
        print("json_data is " + str(json_data) if json_data is not None else "None")
        return None


def load_json(data):
    try:
        return json.loads(data)
    except:
        print("DataError")
        print("data is " + str(data) if data is not None else "None")
        print(type(data) if data is not None else "None")
        return None

# We look at 1 hour delayed data.
delayed_time = datetime.utcnow() - timedelta(hours=2)
title = get_file_title_with_date(delayed_time)
url = get_url("http://data.gharchive.org/", title, "json.gz")
print(url)
response = get_response(url)
data_file = gzip.decompress(response)
data_list = data_file.decode('utf-8').split('\n')

language_urls = []
for data in data_list:
    language_url = get_languages_url_from_json(load_json(data))
    if language_url is not None:
        language_urls.append(language_url)

print(language_urls)

print(get_response(language_urls[0]))
print(type(get_response(language_urls[0])))
