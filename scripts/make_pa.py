import pandas as pd

df = pd.read_csv("../electionnight/pa/live_results.csv", thousands=",")

df2 = pd.crosstab(df["County Name"], df["Candidate Name"], df["Votes"], aggfunc="sum").reset_index()

results = pd.DataFrame()

results["county"] = df2["County Name"].str.title()
df2["county"] = df2["County Name"].str.title()

results.replace({"Mckean":"McKean"}, inplace=True)
df2.replace({"Mckean":"McKean"}, inplace=True)

#is this number going to be found anywhere else (it will be an undercount)
results["ballotscast_2020"] = df2.sum(axis=1)

results.set_index("county", inplace=True)
df2.set_index("County Name", inplace=True)

#results["registered_2020"] = pd.Series([72341, 942747, 44820, 116918, 34238, 272198, 80499, 38861, 488074, 143225, 88273, 3112, 46978, 112093, 380296, 24383, 49699, 22390, 39948, 56579, 187258, 197778, 425405, 20587, 202684, 82389, 3508, 100996, 9837, 22813, 28426, 51795, 32032, 14487, 149406, 354183, 57453, 92642, 249418, 220886, 73763, 25850, 74909, 27361, 118311, 609137, 14013, 227378, 57618, 30027, 1129425, 44668, 11310, 90423, 23700, 49279, 4329, 27212, 26916, 26256, 33299, 31431, 154023, 35687, 253861, 18342, 311188])

results["registered_2020"] = pd.DataFrame([['Adams', 72341], ['Allegheny', 942747], ['Armstrong', 44820], ['Beaver', 116918], ['Bedford', 34238], ['Berks', 272198], ['Blair', 80499], ['Bradford', 38861], ['Bucks', 488074], ['Butler', 143225], ['Cambria', 88273], ['Cameron', 3112], ['Carbon', 46978], ['Centre', 112093], ['Chester', 380296], ['Clarion', 24383], ['Clearfield', 49699], ['Clinton', 22390], ['Columbia', 39948], ['Crawford', 56579], ['Cumberland', 187258], ['Dauphin', 197778], ['Delaware', 425405], ['Elk', 20587], ['Erie', 202684], ['Fayette', 82389], ['Forest', 3508], ['Franklin', 100996], ['Fulton', 9837], ['Greene', 22813], ['Huntingdon', 28426], ['Indiana', 51795], ['Jefferson', 32032], ['Juniata', 14487], ['Lackawanna', 149406], ['Lancaster', 354183], ['Lawrence', 57453], ['Lebanon', 92642], ['Lehigh', 249418], ['Luzerne', 220886], ['Lycoming', 73763], ['Mckean', 25850], ['Mercer', 74909], ['Mifflin', 27361], ['Monroe', 118311], ['Montgomery', 609137], ['Montour', 14013], ['Northampton', 227378], ['Northumberland', 57618], ['Perry', 30027], ['Philadelphia', 1129425], ['Pike', 44668], ['Potter', 11310], ['Schuylkill', 90423], ['Snyder', 23700], ['Somerset', 49279], ['Sullivan', 4329], ['Susquehanna', 27212], ['Tioga', 26916], ['Union', 26256], ['Venango', 33299], ['Warren', 31431], ['Washington', 154023], ['Wayne', 35687], ['Westmoreland', 253861], ['Wyoming', 18342], ['York', 311188]], columns = ["county", "registered_2020"]).set_index("county")

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

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020']).set_index("county")

results.append(statewide).fillna(0).reset_index().rename(columns={'index':'county'}).to_csv("../electionnight/pa/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/pa/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/pa/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.astype({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.reset_index().rename(columns={'index':'county'}).to_csv("../electionnight/pa/results.csv", index=False)
