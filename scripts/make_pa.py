import pandas as pd

df = pd.read_csv("../electionnight/pa/live_results.csv")

df2 = pd.crosstab(df["County Name"], df["Candidate Name"], df["Votes"], aggfunc="sum").reset_index()

results = pd.DataFrame()

results["county"] = df2["County Name"].str.title()

results.replace({"Mckean":"McKean"}, inplace=True)

#is this number going to be found anywhere else (it will be an undercount)
results["ballotscast_2020"] = df2.sum(axis=1)

results["registered_2020"] = pd.Series([72341, 942747, 44820, 116918, 34238, 272198, 80499, 38861, 488074, 143225, 88273, 3112, 46978, 112093, 380296, 24383, 49699, 22390, 39948, 56579, 187258, 197778, 425405, 20587, 202684, 82389, 3508, 100996, 9837, 22813, 28426, 51795, 32032, 14487, 149406, 354183, 57453, 92642, 249418, 220886, 73763, 25850, 74909, 27361, 118311, 609137, 14013, 227378, 57618, 30027, 1129425, 44668, 11310, 90423, 23700, 49279, 4329, 27212, 26916, 26256, 33299, 31431, 154023, 35687, 253861, 18342, 311188])

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df2["BIDEN, JOSEPH ROBINETTE JR"]
results["presvotes_2020"] = df2["TRUMP, DONALD J."] + df2["BIDEN, JOSEPH ROBINETTE JR"] + df2["JORGENSEN, JO"]
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df2["TRUMP, DONALD J."]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020'])

results.append(statewide).fillna(0).to_csv("../electionnight/pa/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/pa/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/pa/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.as_type({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/pa/results.csv")
