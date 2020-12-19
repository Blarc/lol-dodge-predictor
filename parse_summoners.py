import json
import pickle
import pandas as pd
import cassiopeia as cass

from IPython.display import clear_output
from roleidentification import get_roles, pull_data

NUMBER_OF_LINES = 217883
champion_roles = pull_data()
champions_mapper = {champion.id: champion.name for champion in cass.get_champions("EUW")}

summoners = {}

summoners_columns_mapper = {
    'total_games': 0,
    'wins': 1
}

role_names = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']
columns_by_role = ['kills', 'deaths', 'assists', 'gold_earned', 'total_damage_dealt_to_champions',
                   'total_minions_killed', 'vision_score', 'vision_wards_bought', 'total_games', 'wins']

index = len(summoners_columns_mapper)
for role_name in role_names:
    for column in columns_by_role:
        column_key = role_name + '_' + column
        summoners_columns_mapper[column_key] = index
        index += 1

columns_mapper = {}
index = 0

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

        game_duration = float(split[columns_mapper['gameDuration']])

        participant_identities = json.loads(split[columns_mapper['participantIdentities']] \
                                            .replace('\'', '\"'))

        participants = json.loads(split[columns_mapper['participants']] \
                                  .replace('\'', '\"') \
                                  .replace('False', '0') \
                                  .replace('True', '1'))

        champions = []
        for participant in participants:
            champions.append(participant['championId'])

        roles = list(get_roles(champion_roles, champions[0:5]).items())
        roles += list(get_roles(champion_roles, champions[5:10]).items())

        for participantIdentity, participant, role in zip(participant_identities, participants, roles):

            summoner_id = participantIdentity['player']['summonerId']
            role_name = role[0]

            participant_stats = participant['stats']
            win = participant_stats['win']
            kills = participant_stats['kills']
            deaths = participant_stats['deaths']
            assists = participant_stats['assists']
            gold_earned = participant_stats['goldEarned']
            total_damage_dealt_to_champions = participant_stats['totalDamageDealtToChampions']
            total_minions_killed = participant_stats['totalMinionsKilled']
            vision_score = participant_stats['visionScore']
            vision_wards_bought = participant_stats['visionWardsBoughtInGame']

            if summoner_id not in summoners:
                summoners[summoner_id] = {key: 0 for key in summoners_columns_mapper}

            summoners[summoner_id]['wins'] += win
            summoners[summoner_id]['total_games'] += 1
            summoners[summoner_id][role_name + '_wins'] += win
            summoners[summoner_id][role_name + '_total_games'] += 1
            summoners[summoner_id][role_name + '_kills'] += kills / game_duration * 60
            summoners[summoner_id][role_name + '_deaths'] += deaths / game_duration * 60
            summoners[summoner_id][role_name + '_assists'] += assists / game_duration * 60
            summoners[summoner_id][role_name + '_gold_earned'] += gold_earned / game_duration * 60
            summoners[summoner_id][
                role_name + '_total_damage_dealt_to_champions'] += total_damage_dealt_to_champions / game_duration * 60
            summoners[summoner_id][role_name + '_total_minions_killed'] += total_minions_killed / game_duration * 60
            summoners[summoner_id][role_name + '_vision_score'] += vision_score / game_duration * 60
            summoners[summoner_id][role_name + '_vision_wards_bought'] += vision_wards_bought / game_duration * 60

        clear_output(wait=True)
        print(f'{index} / {NUMBER_OF_LINES}')
        index += 1

for summoner in summoners.values():
    for role_name in role_names:
        total_games = summoner[role_name + '_total_games']

        if total_games == 0:
            total_games += 1

        summoner[role_name + '_wins'] /= total_games
        summoner[role_name + '_kills'] /= total_games
        summoner[role_name + '_deaths'] /= total_games
        summoner[role_name + '_assists'] /= total_games
        summoner[role_name + '_gold_earned'] /= total_games
        summoner[role_name + '_total_damage_dealt_to_champions'] /= total_games
        summoner[role_name + '_total_minions_killed'] /= total_games
        summoner[role_name + '_vision_score'] /= total_games
        summoner[role_name + '_vision_wards_bought'] /= total_games

print(f'Number of summoners: {len(summoners)}')

print('Saving to pickle...')
with open('data/processed_data/summoners.pickle', 'wb') as handle:
    pickle.dump(summoners, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Saved to \'data/processed_data/summoners.pickle\'')

print('Saving to csv...')
pd.DataFrame.from_dict(data=summoners, orient='index').to_csv('data/processed_data/summoners.csv', header=True)
print('Saved to \'data/processed_data/summoners.csv\'')
