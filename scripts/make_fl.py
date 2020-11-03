import pandas as pd

df = pd.read_csv("../electionnight/fl/live_results.txt", sep="\t", usecols = ["PartyCode", "RaceName", "CountyName", "CanNameFirst", "CanVotes"])

#get results for US President
df = df[(df.RaceName=="President of the United States")]

df2 = pd.crosstab(index=df.CountyName, columns=df.CanNameFirst, values=df.CanVotes, aggfunc="sum").reset_index()

results = pd.DataFrame()

results["county"] = df2["CountyName"].str.title()

results.replace({"Desoto":"DeSoto"}, inplace=True)

#is this number going to be found anywhere else (it will be an undercount)
results["ballotscast_2020"] = df2.sum(axis=1)

#need to double check this number (this is from the bookclosing report, not sure if it will be more updated before election night)
results["registered_2020"] = pd.Series([190433, 16933, 124653, 17742, 452424, 1266991, 8709, 152142, 117092, 164745, 231708, 44239, 17819, 10595, 664211, 232238, 91916, 8485, 31155, 12516, 7097, 10829, 8098, 13111, 19122, 146893, 66317, 934346, 11489, 124586, 29857, 10236, 4568, 264691, 489187, 217454, 30099, 4601, 11758, 273427, 264614, 118472, 1564297, 56910, 72223, 150654, 22394, 866460, 239027, 1020222, 393392, 711462, 471241, 50692, 145810, 340092, 335172, 210059, 223640, 105612, 27728, 12779, 7718, 398530, 22909, 58057, 17191])

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df2["Biden"]
#results["biden_2020"] = df2["Clinton"] #remove this and replace with above on election night
results["presvotes_2020"] = df2["Trump"] + df2["Biden"] + df2["Jorgensen"] + df2["De La Fuente"] + df2["La Riva"] + df2["Hawkins"] + df2["Blakenship"]
#results["presvotes_2020"] = df2["Clinton"] + df2["Castle"] + df2["Johnson"] + df2["Trump"] + df2["De La Fuente"] + df2["Stein"] #remove this and replace with above on election night
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df2["Trump"]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020'])

results.append(statewide).fillna(0).to_csv("../electionnight/fl/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/fl/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/fl/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results.to_csv("../electionnight/fl/results.csv")
