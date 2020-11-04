import pandas as pd

#get results for US President
df = pd.read_excel("../electionnight/oh/live_results.xlsx", sheet_name=2, skiprows=1, usecols=[0, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], names=["County Name", "Registered Voters", "Ballots Counted", 'Biden', 'Boddie', 'Carroll', 'Hawkins', 'Hoefling', 'Hunter', 'Jorgensen', 'Simmons', 'Trump', 'Wells'])

#drop first two rows
df = df.iloc[2:].reset_index(drop=True)

results = pd.DataFrame()

results["county"] = df["County Name"].str.title()

results["ballotscast_2020"] = df['Biden'] + df['Boddie'] + df['Carroll'] + df['Hawkins'] + df['Hoefling'] + df['Hunter'] + df['Jorgensen'] + df['Simmons'] + df['Trump'] + df['Wells']

results["registered_2020"] = df["Registered Voters"]

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df["Biden"]
results["presvotes_2020"] = df["Biden"] + df["Hawkins"] + df["Jorgensen"] + df["Trump"]
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df["Trump"]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020'])

results.append(statewide).fillna(0).to_csv("../electionnight/oh/results_2020.csv", index=False)
results_2016 = pd.read_csv("../electionnight/oh/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/oh/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.astype({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/oh/results.csv")
