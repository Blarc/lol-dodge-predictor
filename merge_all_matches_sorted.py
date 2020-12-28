import pandas as pd

match_df = pd.read_pickle('data/raw_data/match_data_version1.pickle')
winner_df = pd.read_pickle('data/raw_data/match_winner_data_version1.pickle')
loser_df = pd.read_pickle('data/raw_data/match_loser_data_version1.pickle')


match_winner_merged_df = pd.merge(match_df, winner_df, on='gameId', how='left')
match_loser_merged_df = pd.merge(match_df, loser_df, on='gameId', how='left')
match_all_merged_df = pd.concat([match_loser_merged_df, match_winner_merged_df], ignore_index=True)

print("Sorting...")
match_all_merged_df.sort_values(by='gameCreation', inplace=True, ignore_index=True)
print("Sorted!")

print("Saving...")
match_all_merged_df.to_csv('data/raw_data/match_all_merged_sorted.csv', sep=';')
print("Saved!")

match_all_merged_df.head()
