from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import gzip
import json
import urllib
import configparser
import db


# Parse configs
config = configparser.ConfigParser()
config.read('../resource/config.txt')


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


def get_repo_id_from_json(json_data):
    try:
        return json_data["repo"]["id"]
    except KeyError: # missing either "repo" or "id" keys
        #print("KeyError")
        return None
    except TypeError: # "None" or other non-json datatype within json_data
        #print("TypeError")
        return None
    except Exception as e:
        print("Unhandled error: " + e)
        return None


def get_repo_name_from_json(json_data):
    try:
        return json_data["repo"]["name"]
    except KeyError: # missing either "repo" or "name" keys
        #print("KeyError")
        return None
    except TypeError: # "None" or other non-json datatype within json_data
        #print("TypeError")
        return None
    except Exception as e:
        print("Unhandled error: " + e)
        return None


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


def build_repo_metadata(repo_id, repo_name, language_url, number_lines):
    repo_metadata = dict()
    repo_metadata["repo_id"] = repo_id
    repo_metadata["repo_name"] = repo_name
    repo_metadata["language_url"] = language_url
    repo_metadata["number_lines"] = number_lines

    return repo_metadata


def build_entry(timestamp, repo_metadata, languages):
    entry = dict()
    entry["timestamp"] = timestamp
    entry["repo_metadata"] = repo_metadata
    entry["languages"] = languages

    return entry


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
counter = 0
print("Total lines of data is " + str(len(data_list)))

for data in data_list:
    loaded_json = load_json(data)

    repo_id = get_repo_id_from_json(loaded_json)
    repo_name = get_repo_name_from_json(loaded_json)

    language_url = get_languages_url_from_json(loaded_json)
    if language_url is not None:
        # Only process languages from this url if it's not yet processed
        if language_url not in language_urls:
            try:
                language_frequency = dict()

                languages = load_json(get_response(language_url, True).decode('ascii'))

                # Get total lines
                number_lines = sum(languages.values())

                for language in languages:
                    # Insert proportion of lines in this language into language_frequency
                    language_frequency[language] = languages[language]/number_lines

                # Build entry and insert it to the db
                repo_metadata = build_repo_metadata(repo_id, repo_name, language_url, number_lines)
                entry = build_entry(delayed_time, repo_metadata, language_frequency)
                database = db.Database()
                database.insert(entry)

                language_urls.add(language_url)
            except urllib.error.HTTPError as e:
                print(language_url + " failed with " + str(e))
            except Exception as e:
                print("Unhandled error: " + str(e))

print("Total unique repositories read is " + str(len(language_urls)))

total_lines = sum(language_frequency.values())
for language in language_frequency:
    language_frequency[language] /= total_lines
print(str(language_frequency))

