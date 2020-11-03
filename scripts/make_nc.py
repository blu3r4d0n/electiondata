import pandas as pd

df = pd.read_csv("../electionnight/nc/live_results.txt", sep="\t", usecols = ['County', 'Contest Name', 'Choice', 'Total Votes'])

#get results for US President
df = df[df["Contest Name"] == "US PRESIDENT"]

df2 = pd.crosstab(df["County"], df["Choice"], df["Total Votes"], aggfunc="sum").reset_index()

results = pd.DataFrame()

results["county"] = df2["County"].str.title()

results.replace({"Mcdowell":"McDowell"}, inplace=True)

#is this number going to be found anywhere else (it will be an undercount)
results["ballotscast_2020"] = df2.sum(axis=1)

#need to double check this number (using Oct 31 registration data, active/inactive/temporary voters)
results["registered_2020"] = pd.Series([110601, 24891, 7612, 16510, 19410, 12388, 33999, 13276, 22863, 114610, 207157, 58146, 150403, 54547, 8160, 51891, 15494, 108606, 57724, 22697, 10275, 9127, 67619, 36801, 72832, 226965, 21812, 30129, 113523, 31448, 30547, 244340, 35661, 271771, 47495, 151635, 8333, 6069, 40060, 11389, 383465, 37792, 82006, 46373, 87486, 15007, 33189, 3171, 130637, 29622, 142963, 7399, 38606, 38421, 62436, 27200, 17228, 16481, 29813, 791942, 11107, 17021, 73961, 68482, 177124, 13929, 117125, 112113, 9769, 28555, 44786, 9731, 27755, 123330, 16497, 94641, 29325, 76444, 61706, 97198, 45882, 37798, 22017, 42851, 31834, 47007, 10084, 26500, 2376, 167713, 29609, 794942, 13518, 8310, 45101, 76040, 43778, 57088, 24696, 14160])

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df2["Joseph R. Biden"]
results["presvotes_2020"] = df2["Don Blankenship"] + df2["Donald J. Trump"] + df2["Howie Hawkins"] + df2["Jo Jorgensen"] + df2["Joseph R. Biden"]
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df2["Donald J. Trump"]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020'])

results.append(statewide).fillna(0).to_csv("../electionnight/nc/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/nc/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/nc/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.astype({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/nc/results.csv")
