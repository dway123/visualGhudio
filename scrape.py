from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import gzip
import json
import urllib
import configparser
from pymongo import MongoClient


# Parse configs
config = configparser.ConfigParser()
config.read('config.txt')


def get_file_title_with_date(target_date) :
    return target_date.strftime("%Y-%m-%d-") + target_date.strftime("%H").replace('0', '', 1)


def get_url(prefix, file_title, extension=None):
    return_url = prefix + file_title

    if extension is not None:
        return_url += ('.' + extension)

    return return_url


def get_response(url, auth):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    if auth:
        if 'github.com' in config and 'PersonalToken' in config['github.com']:
            request.add_header('Authorization', "token " + config['github.com']['PersonalToken'])
        else:
            raise AttributeError('No personal token found in configuration file. Add your personal token in config.txt file.')

    response = urlopen(request)

    return response.read()


def get_languages_url_from_json(json_data):
    try:
        return json_data["payload"]["pull_request"]["head"]["repo"]["languages_url"]
    except KeyError: # Likely missing "pull_request" key, but may be others in the json_data
        #print("KeyError")
        return None
    except TypeError: # "None" or other non-json datatype within json_data
        #print("TypeError")
        return None
    except Exception as e:
        print("Unhandled error: " + e)
        return None


def load_json(data):
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError: # Wrong data format from nonconformant input data 
        #print("DataError")
        return None
    except Exception as e:
        print("Unhandled error: " + e)
        return None


def mongodb_test():
    uri = config['mongodb.com']['ConnectionString']
    client = MongoClient(uri)
    db = client['sf-031']
    collection = db['languages']
    post = {"test" : "hello"}
    post_id = collection.insert_one(post).inserted_id
    print(post_id)


# We look at 1 hour delayed data.
delayed_time = datetime.utcnow() - timedelta(hours=2)
title = get_file_title_with_date(delayed_time)
url = get_url("http://data.gharchive.org/", title, "json.gz")
print(url)
response = get_response(url, False)
data_file = gzip.decompress(response)
data_list = data_file.decode('utf-8').split('\n')


# Set up for getting language distribution
language_urls = set()
language_frequency = dict()
counter = 0
print("Total lines of data is " + str(len(data_list)))

for data in data_list:
    language_url = get_languages_url_from_json(load_json(data))
    if language_url is not None:
        # Only process languages from this url if it's not yet processed
        if language_url not in language_urls:
            try:
                languages = load_json(get_response(language_url, True).decode('ascii'))
                #print(counter)
                #counter += 1
                total_lines = sum(languages.values())
                for language in languages:
                    # Insert proportion of lines in this language into language_frequency
                    if language not in language_frequency:
                        language_frequency[language] = 0
                    language_frequency[language] += languages[language]/total_lines

                language_urls.add(language_url)
            except urllib.error.HTTPError as e:
                print(language_url + " failed with " + str(e))
            except Exception as e:
                print("Unhandled error: " + e)

print("Total unique repositories read is " + str(len(language_urls)))

total_lines = sum(language_frequency.values())
for language in language_frequency:
    language_frequency[language] /= total_lines
print(str(language_frequency))
