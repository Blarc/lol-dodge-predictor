import json
import pickle
import pandas as pd
from roleidentification import get_roles, pull_data

NUMBER_OF_LINES = 217883

role_index_mapper = {
    'TOP': 0,
    'JUNGLE': 1,
    'MIDDLE': 2,
    'BOTTOM': 3,
    'UTILITY': 4
}

champion_roles = pull_data()
columns_mapper = {}

index = 0
matches_index = 0

matches = {}

with open('data/processed_data/summoners.pickle', 'rb') as inpickle:
    summoners_parsed = pickle.load(inpickle)

with open('data/raw_data/match_all_merged.csv', encoding='utf8') as infile:
    for line in infile:
        split = line.rstrip('\n').split(';')
        if index == 0:
            columns_mapper = {key: value for value, key in enumerate(split)}
            index += 1
            continue

        queue_id = float(split[columns_mapper['queueId']])
        if queue_id != 420:
            index += 1
            continue

        win = split[columns_mapper['win']] == 'Win'

        participant_identities = json.loads(split[columns_mapper['participantIdentities']]
                                            .replace('\'', '\"'))

        participants = json.loads(split[columns_mapper['participants']]
                                  .replace('\'', '\"')
                                  .replace('False', '0')
                                  .replace('True', '1'))

        champions = []
        for participant in participants:
            champions.append(participant['championId'])

        roles = list(get_roles(champion_roles, champions[0:5]).items())
        roles += list(get_roles(champion_roles, champions[5:10]).items())

        teams = {
            100: [None] * 5,
            200: [None] * 5
        }

        win = {}

        for participantIdentity, participant, role in zip(participant_identities, participants, roles):
            summoner_id = participantIdentity['player']['summonerId']
            team_id = participant['teamId']

            summoner = summoners_parsed[summoner_id]
            role_index = role_index_mapper[role[0]]

            teams[team_id][role_index] = summoner
            win[team_id] = participant['stats']['win']

        match = {}
        for team, win in zip(teams.values(), win.values()):
            for role, player in zip(role_index_mapper.keys(), team):
                for key, value in player.items():
                    match[role + '_' + key] = value

            match['win'] = win
            matches[matches_index] = match
            matches_index += 1

        print(f'{index} / {NUMBER_OF_LINES}')
        index += 1

print(f'Number of matches: {len(matches)}')

print('Saving to pickle...')
with open('data/processed_data/matches.pickle', 'wb') as handle:
    pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Saved to \'data/processed_data/matches.pickle\'')

print('Saving to csv...')
pd.DataFrame.from_dict(data=matches, orient='index').to_csv('data/processed_data/matches.csv', header=True)
print('Saved to \'data/processed_data/matches.csv\'')
