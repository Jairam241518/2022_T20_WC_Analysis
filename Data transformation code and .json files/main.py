import pandas as pd
import json

# MATCH SUMMARY
with open('t20_wc_match_results.json') as f1:
    data = json.load(f1)
df_match = pd.DataFrame(data[0]['matchSummary'])
df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)

match_id_dict = {}
for index, row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']

    match_id_dict[key1] = row['match_id']
    match_id_dict[key2] = row['match_id']

df_match.to_csv('t20_wc_match_results.csv', index = False)


# BATTING SUMMARY
with open('t20_wc_batting_summary.json') as f2:
    data_batting = json.load(f2)
    all_records = []
    for rec in data_batting:
        all_records.extend(rec['battingSummary'])
df_batting = pd.DataFrame(all_records)
df_batting['out/not_out'] = df_batting.dismissal.apply(lambda x: "out" if len(x) > 0 else "not_out")
df_batting.drop(columns=["dismissal"], inplace=True)

df_batting['match_id'] = df_batting["match"].map(match_id_dict)
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0', ''))
df_batting.to_csv('t20_wc_batting_summary.csv', index = False)

#BOWLING SUMMARY

with open('t20_wc_bowling_summary.json') as f3:
    data_bowling = json.load(f3)
    all_records_bowling = []
    for rec in data_bowling:
        all_records_bowling.extend(rec['bowlingSummary'])

df_bowling = pd.DataFrame(all_records_bowling)
df_bowling['match_id'] = df_bowling['match'].map(match_id_dict)
df_bowling.to_csv('t20_wc_bowling_summary.csv', index = False)

#PLAYER INFORMATION

with open('t20_wc_player_info.json') as f4:
    data_player = json.load(f4)

df_players = pd.DataFrame(data_player)

print(df_players.shape)

df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))

df_players.to_csv('t20_wc_player_info_no_images.csv', index = False)
