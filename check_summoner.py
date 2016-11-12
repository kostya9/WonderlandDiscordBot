import urllib.request
import urllib.parse
import json
import re

api_key= json.loads(open('settings.json').read())["api_code"]
summoner_byname_uri = 'https://ru.api.pvp.net/api/lol/RU/v1.4/summoner/by-name/'
current_game_uri = 'https://ru.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/RU/'

class CouldNotFindSummonerException(LookupError):
    '''raise this when there's a lookup error for my app'''

def check_if_summoner_ingame(message):
    matches = re.search('(?<=#check ).+', str(message))
    summonerName = matches.group(0)
    id = get_summoner_id(summonerName)
    return get_game_status(id)


def get_summoner_id(name):
    name = "".join(name.split())
    uri = add_api_key(summoner_byname_uri + urllib.parse.quote_plus(name.encode('utf-8')))
    try:
        json_response = urllib.request.urlopen(uri).read().decode("utf8")
    except urllib.request.HTTPError as e:
        if e.code == 404:
            raise CouldNotFindSummonerException('Could not find that guy')

    print("Server responded : " + json_response)
    data = json.loads(json_response)
    return data[name.lower()]["id"]

def get_game_status(id):
    uri = add_api_key(current_game_uri + str(id))
    try:
        response_info = urllib.request.urlopen(uri)
    except urllib.request.HTTPError as e:
        if e.code == 404:
            return False
    http_code = response_info.getcode()
    if(http_code == 200):
        return True
    return False


def add_api_key(uri):
    return uri + '?api_key=' + str(api_key)