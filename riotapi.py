from typing import Dict

import requests

API_TOKEN = "RGAPI-689b65b3-cb12-4716-9874-970c2191e688"
API_BASE_URL = "https://euw1.api.riotgames.com/lol/"
SUMMONER_BY_NAME_URL = "summoner/v4/summoners/by-name/{0}"
MATCH_BY_ID_URL = "match/v4/matches/{0}"
MATCH_LISTS_BY_ENCRYPTED_ACCOUNT_ID_URL = "match/v4/matchlists/by-account/{0}"


def get_summoner_by_username(username: str):
    url = create_url(SUMMONER_BY_NAME_URL, username)
    return get(url)


def get_match_references_by_account_id(account_id: str):
    url = create_url(MATCH_LISTS_BY_ENCRYPTED_ACCOUNT_ID_URL, account_id)
    return get(url)


def get_match_references_by_username(username: str):
    account_id = get_summoner_by_username(username)['accountId']
    return get_match_references_by_account_id(account_id)


def get_match_by_id(game_id: str):
    url = create_url(MATCH_BY_ID_URL, game_id)
    return get(url)


def create_url(url: str, parameter: str) -> str:
    temp = url.format(parameter)
    return API_BASE_URL + temp


def create_header() -> Dict[str, str]:
    return {
        'X-Riot-Token': API_TOKEN
    }


def get(url):
    return requests.get(url, headers=create_header()).json()
