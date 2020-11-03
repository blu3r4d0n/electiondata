import pandas as pd

#get results for ballots cast
df1 = pd.read_excel("../electionnight/ga/live_results.xlsx", sheet_name=1)

#get results for US President
df2 = pd.read_excel("../electionnight/ga/live_results.xlsx", sheet_name=2, skiprows=2, usecols=[0, 1, 6, 11, 17], names=["County", "Registered Voters", "Trump Total Votes", "Biden Total Votes", "Pres Total Votes"])

results = pd.DataFrame()

results["county"] = df2["County"].str.title()

results.replace({"Dekalb":"DeKalb", "Mcduffie":"McDuffie", "Mcintosh":"McIntosh"}, inplace=True)

results["ballotscast_2020"] = df1["Ballots Cast"]

results["registered_2020"] = df1["Registered Voters"]
#results["registered_2020"] = df2["Registered Voters"]

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df2["Biden Total Votes"]
results["presvotes_2020"] = df2["Pres Total Votes"]
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df2["Trump Total Votes"]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

#remove the "total" row
results.drop(results.tail(1).index,inplace=True)

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020'])

results.append(statewide).fillna(0).to_csv("../electionnight/ga/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/ga/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/ga/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.as_type({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/ga/results.csv")
