import pandas as pd

match_df = pd.read_pickle('data/raw_data/match_data_version1.pickle')
print(len(match_df))
winner_df = pd.read_pickle('data/raw_data/match_winner_data_version1.pickle')
print(len(winner_df))
# loser_df = pd.read_pickle('data/raw_data/match_loser_data_version1.pickle')
# print(len(loser_df))

match_winner_merged_df = pd.merge(match_df, winner_df, on='gameId', how='left')
# match_loser_merged_df = pd.merge(match_df, loser_df, on='gameId', how='left')
# match_all_merged_df = pd.concat([match_loser_merged_df, match_winner_merged_df], ignore_index=True)

print("Sorting...")
match_winner_merged_df.sort_values(by='gameCreation', inplace=True, ignore_index=True)
print("Sorted!")

print("Saving...")
match_winner_merged_df.to_csv('data/raw_data/match_all_merged_sorted.csv', sep=';')
print("Saved!")

# Length: 108941
print(f"Length: {len(match_winner_merged_df)}")
