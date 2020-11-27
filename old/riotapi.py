from typing import Dict
from time import sleep

import requests

API_TOKEN = "RGAPI-8b277fda-962a-4b15-802a-4793a034c9f5"
API_BASE_URL = "https://euw1.api.riotgames.com/lol/"
SUMMONER_BY_NAME_URL = "summoner/v4/summoners/by-name/{0}"
MATCH_BY_ID_URL = "match/v4/matches/{0}"
MATCH_LISTS_BY_ENCRYPTED_ACCOUNT_ID_URL = "match/v4/matchlists/by-account/{0}"
PLAYERS_IN_DIAMOND1 = "league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1"
SUMMONER_WINRATE = "league/v4/entries/by-summoner/{0}"

# query params
QUERY_PARAM_INDEX = "endIndex={0}&beginIndex={1}"
QUERY_PARAM_QUEUE = "queue={0}"

# static data
QUEUE_TYPE_RANKED = 420


def get_summoner_by_username(username: str):
    url = create_url(SUMMONER_BY_NAME_URL, username)
    return get(url)


def get_summoner_winrate(summoner_id: str):
    url = create_url(SUMMONER_WINRATE, summoner_id)
    entries = get(url)
    for entry in entries:
        if entry['queueType'] == 'RANKED_SOLO_5x5':
            wins = entry['wins']
            losses = entry['losses']
            return wins / (wins + losses)


def get_match_references_by_account_id(account_id: str, start_index=0, end_index=100):
    url = create_url(MATCH_LISTS_BY_ENCRYPTED_ACCOUNT_ID_URL, account_id)
    url = add_query_param(url, QUERY_PARAM_QUEUE.format(QUEUE_TYPE_RANKED))
    url = add_query_param(url, create_index_query_param(start_index, end_index))
    return get(url)['matches']


def get_match_references_by_username(username: str, start_index=0, end_index=100):
    account_id = get_summoner_by_username(username)['accountId']
    return get_match_references_by_account_id(account_id, start_index, end_index)


def get_match_by_id(game_id: str):
    url = create_url(MATCH_BY_ID_URL, game_id)
    return get(url)


def get_players_in_diamond1():
    url = create_url(PLAYERS_IN_DIAMOND1, "")
    return get(url)


def create_index_query_param(start_index=0, end_index=100):
    return QUERY_PARAM_INDEX.format(end_index, start_index)


def add_query_param(url: str, param: str):
    if '?' in url:
        return url + '&' + param

    return url + '?' + param


def create_url(url: str, parameter: str) -> str:
    temp = url.format(parameter)
    return API_BASE_URL + temp


def create_header() -> Dict[str, str]:
    return {
        'X-Riot-Token': API_TOKEN
    }


def get(url):
    result = requests.get(url, headers=create_header())

    while result.status_code != 200:

        if result.status_code == 403:
            print(f"ERROR: {result.status_code}")
            global API_TOKEN
            API_TOKEN = str(input("Insert new api key: "))
            print(f"API_TOKEN set to: {API_TOKEN}")

        elif result.status_code == 404:
            print(f"ERROR 404: skipping...")
            return "404"

        else:
            print(f"ERROR: {result.status_code}. Sleeping for 120s.")
            sleep(121)

        print("Retrying...")
        result = requests.get(url, headers=create_header())

    # sleep for 1.3 seconds because api only allows 100 requests / 120 seconds
    sleep(2)
    return result.json()
