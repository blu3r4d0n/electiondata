import pandas as pd

#get results for ballots cast
#df1 = pd.read_excel("../electionnight/ga/live_results.xlsx", sheet_name=1)

#get results for US President
df2 = pd.read_excel("../electionnight/ga/live_results.xlsx", sheet_name=1, skiprows=2, usecols=[0, 5, 10, 16], names=["County", "Trump Total Votes", "Biden Total Votes", "Pres Total Votes"])

results = pd.DataFrame()

results["county"] = df2["County"].str.title()

results.replace({"Dekalb":"DeKalb", "Mcduffie":"McDuffie", "Mcintosh":"McIntosh"}, inplace=True)

#this is an undercount because they are not reporting it
results["ballotscast_2020"] = df2["Pres Total Votes"]

results["registered_2020"] = pd.Series([11440, 4801, 6726, 2258, 26742, 12905, 55694, 74380, 9892, 11317, 108126, 7558, 11302, 11170, 30651, 44737, 16570, 17195, 3187, 35141, 6328, 83866, 45785, 6562, 202999, 3943, 14183, 190605, 76848, 2053, 194338, 4345, 537659, 25165, 25087, 107656, 10650, 102262, 8536, 12560, 11682, 21557, 16726, 547802, 11464, 5966, 61402, 101613, 7340, 2170, 44372, 12330, 13844, 6148, 20399, 92427, 60749, 164279, 15170, 808742, 22315, 2040, 61947, 36431, 15441, 14197, 582917, 28318, 128535, 5835, 20692, 25690, 16942, 7772, 172241, 105587, 6124, 52010, 10434, 8495, 11350, 5075, 5610, 20406, 12872, 5496, 32874, 22930, 35970, 6182, 9683, 75535, 22412, 7079, 20737, 4922, 15083, 9320, 15336, 3920, 13481, 21151, 5467, 14843, 22340, 132029, 79098, 30051, 10848, 115297, 18164, 23820, 12735, 13825, 24256, 5712, 16000, 1553, 13074, 4338, 135428, 65573, 2890, 9610, 5937, 46088, 18078, 2909, 18033, 4567, 1246, 12216, 5405, 6076, 6625, 30218, 24551, 16227, 10189, 4248, 43169, 5604, 6308, 19235, 18187, 43050, 70129, 20580, 3789, 12994, 18164, 1713, 3169, 20630, 54779, 4562, 6836, 6484, 13847])

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
results = results.astype({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/ga/results.csv")
