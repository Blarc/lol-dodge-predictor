from riotapi import get_match_by_id
import pandas as pd


def parse_match_reference(match_reference):
    return match_reference['champion'], match_reference['role'], match_reference['lane'], match_reference['gameId']


def get_match_by_id_safe(game_id):
    try:
        game = get_match_by_id(game_id)
    except:
        print(f"Error. Skipping game {game_id}")
        return None

    if game == "404":
        return None

    return game


def find_participant_by_champion(game, champion):
    participants = game['participants']
    for p in participants:
        if p['championId'] == champion:
            return p


def parse_participant_data(game, champion, role, lane, win_rate):
    participant = find_participant_by_champion(game, champion)
    return parse_participant(champion, role, lane, game, participant, win_rate)


def parse_participant(champion, role, lane, game, participant, win_rate):
    participant_stats = participant['stats']
    return [champion, role, lane, participant_stats['win'], participant_stats['kills'], participant_stats['deaths'],
            participant_stats['assists'], participant_stats['totalDamageDealtToChampions'],
            participant_stats['visionScore'], participant_stats['goldEarned'], participant_stats['totalMinionsKilled'],
            game['gameDuration'], win_rate], participant_stats['win']


def parse_teammates(game, champion):
    participant = find_participant_by_champion(game, champion)
    team_id = participant['teamId']

    participant_ids = []
    for participant in game['participants']:
        if participant['championId'] != champion and participant['teamId'] == team_id:
            participant_ids.append(participant['participantId'])

    teammates = []
    participant_identities = game['participantIdentities']
    for participant_identity in participant_identities:
        if participant_identity['participantId'] in participant_ids:
            teammates.append(participant_identity['player']['accountId'])

    return teammates


def save_match_to_csv(match_list, path):
    dataset = pd.DataFrame(match_list)
    dataset.columns = ['champion', 'role', 'lane', 'win', 'kills', 'deaths', 'assists',
                       'total_damage_dealt_to_champions', 'vision_score', 'gold_earned', 'total_minions_killed',
                       'game_duration', 'win_rate']
    dataset.to_csv(path, index=False, header=True)
    print(f"Saved to {path}")


def save_match_teammates_to_csv(match_teammates, path):
    dataset = pd.DataFrame(match_teammates)
    dataset.columns = ['teammate_1', 'teammate_2', 'teammate_3', 'teammate_4', 'win']
    dataset.to_csv(path, index=False, header=True)
    print(f"Saved to {path}")


def save_teammates_to_csv(teammates, path):
    dataset = pd.DataFrame(teammates)
    dataset.to_csv(path, index=False, header=True)
    print(f"Saved to {path}")
