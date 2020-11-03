import pandas as pd

#used libreoffice to convert xls to csv
df = pd.read_csv("../electionnight/mi/live_results.csv", sep="\t")

#get results for US President
df = df[(df.OfficeDescription=="President of the United States 4 Year Term (1) Position")]

df2 = pd.crosstab(index=df.CountyName, columns=df.CandidateLastName, values=df.CandidateVotes, aggfunc="sum").reset_index()

results = pd.DataFrame()

results["county"] = df2["CountyName"].str.title()
df2["CountyName"] = df2["CountyName"].str.title()

results.replace({"Gd. Traverse":"Grand Traverse"}, inplace=True)
df2.replace({"Gd. Traverse":"Grand Traverse"}, inplace=True)

#is this number going to be found anywhere else (it will be an undercount)
results["ballotscast_2020"] = df2.sum(axis=1)

results.set_index("county", inplace=True)
df2.set_index("CountyName", inplace=True)

#need to double check this number
registered = pd.DataFrame([['Alcona', 9868], ['Alger', 7594], ['Allegan', 93821], ['Alpena', 24854], ['Antrim', 21998], ['Arenac', 12716], ['Baraga', 6683], ['Barry', 49758], ['Bay', 84726], ['Benzie', 16469], ['Berrien', 134881], ['Branch', 33727], ['Calhoun', 106256], ['Cass', 44566], ['Charlevoix', 23708], ['Cheboygan', 22597], ['Chippewa', 26179], ['Clare', 25233], ['Clinton', 62211], ['Crawford', 12001], ['Delta', 31338], ['Dickinson', 23382], ['Eaton', 87864], ['Emmet', 30587], ['Genesee', 349041], ['Gladwin', 21896], ['Gogebic', 14320], ['Grand Traverse', 80921], ['Gratiot', 28289], ['Hillsdale', 36498], ['Houghton', 26532], ['Huron', 26187], ['Ingham', 213783], ['Ionia', 46868], ['Iosco', 22568], ['Iron', 10476], ['Isabella', 46187], ['Jackson', 122216], ['Kalamazoo', 210346], ['Kalkaska', 16003], ['Kent', 499980], ['Keweenaw', 2052], ['Lake', 9975], ['Lapeer', 71977], ['Leelanau', 21366], ['Lenawee', 78958], ['Livingston', 161087], ['Luce', 4556], ['Mackinac', 10119], ['Macomb', 692232], ['Manistee', 20953], ['Marquette', 54726], ['Mason', 24704], ['Mecosta', 31148], ['Menominee', 20238], ['Midland', 69519], ['Missaukee', 12040], ['Monroe', 130456], ['Montcalm', 47795], ['Montmorency', 8572], ['Muskegon', 140862], ['Newaygo', 39726], ['Oakland', 1033085], ['Oceana', 21190], ['Ogemaw', 17848], ['Ontonagon', 5751], ['Osceola', 18406], ['Oscoda', 7290], ['Otsego', 22985], ['Ottawa', 220133], ['Presque Isle', 11545], ['Roscommon', 22951], ['Saginaw', 156502], ['Sanilac', 31604], ['Schoolcraft', 7227], ['Shiawassee', 55825], ['St. Clair', 134201], ['St. Joseph', 47356], ['Tuscola', 42846], ['Van Buren', 60690], ['Washtenaw', 317585], ['Wayne', 1403004], ['Wexford', 27441]], columns = ["county", "registered_2020"]).set_index("county")
#registered = pd.DataFrame([['Alcona', 9347], ['Alger', 7337], ['Allegan', 83976], ['Alpena', 23549], ['Antrim', 20425], ['Arenac', 12151], ['Baraga', 6428], ['Barry', 45336], ['Bay', 80236], ['Benzie', 15088], ['Berrien', 127768], ['Branch', 31518], ['Calhoun', 100662], ['Cass', 40527], ['Charlevoix', 22144], ['Cheboygan', 21318], ['Chippewa', 24279], ['Clare', 23386], ['Clinton', 57040], ['Crawford', 11343], ['Delta', 29395], ['Dickinson', 22250], ['Eaton', 81665], ['Emmet', 28547], ['Genesee', 331057], ['Gladwin', 21084], ['Gogebic', 13953], ['Grand Traverse', 73819], ['Gratiot', 26463], ['Hillsdale', 33922], ['Houghton', 24944], ['Huron', 25207], ['Ingham', 203049], ['Ionia', 43247], ['Iosco', 21293], ['Iron', 9680], ['Isabella', 43606], ['Jackson', 111923], ['Kalamazoo', 195448], ['Kalkaska', 14720], ['Kent', 453052], ['Keweenaw', 1957], ['Lake', 9217], ['Lapeer', 66834], ['Leelanau', 20127], ['Lenawee', 73564], ['Livingston', 145712], ['Luce', 4315], ['Mackinac', 9495], ['Macomb', 630577], ['Manistee', 19720], ['Marquette', 51204], ['Mason', 22833], ['Mecosta', 27742], ['Menominee', 19163], ['Midland', 65519], ['Missaukee', 10889], ['Monroe', 118691], ['Montcalm', 42907], ['Montmorency', 7975], ['Muskegon', 128799], ['Newaygo', 35833], ['Oakland', 957357], ['Oceana', 19526], ['Ogemaw', 16596], ['Ontonagon', 5661], ['Osceola', 17350], ['Oscoda', 6768], ['Otsego', 21009], ['Ottawa', 197977], ['Presque Isle', 10893], ['Roscommon', 21706], ['Saginaw', 150018], ['St. Clair', 124354], ['St. Joseph', 43970], ['Sanilac', 29510], ['Schoolcraft', 6791], ['Shiawassee', 52779], ['Tuscola', 40793], ['Van Buren', 55350], ['Washtenaw', 285272], ['Wayne', 1339831], ['Wexford', 25289]], columns = ["county", "registered_2020"]).set_index("county") #remove this and replace with the above on election night

results = pd.concat([results, registered], axis=1)

results["turnout_2020"] = results["ballotscast_2020"]/results["registered_2020"]
results["biden_2020"] = df2["Biden"]
#results["biden_2020"] = df2["Clinton"] #remove this and replace with the above on election night
results["presvotes_2020"] = df2["Biden"] + df2["Trump"] + df2["Jorgensen"] + df2["Blankenship"] + df2["Hawkins"] + df2["De La Fuente"]
#results["presvotes_2020"] = df2["Trump"] + df2["Clinton"] + df2["Johnson"] + df2["Castle"] + df2["Stein"] + df2["Soltysik"] #remove this and replace with the above on election night
results["bidenpct_2020"] = results["biden_2020"]/results["presvotes_2020"]
results["trump_2020"] = df2["Trump"]
results["trumppct_2020"] = results["trump_2020"]/results["presvotes_2020"]

if results["presvotes_2020"].sum() == 0:
	statewide_bidenpct_2020 = 0
	statewide_trumppct_2020 = 0
else:
	statewide_bidenpct_2020 = results["biden_2020"].sum()/results["presvotes_2020"].sum()
	statewide_trumppct_2020 = results["trump_2020"].sum()/results["presvotes_2020"].sum()

statewide = pd.DataFrame([["STATEWIDE", results["ballotscast_2020"].sum(), results["registered_2020"].sum(), results["ballotscast_2020"].sum()/results["registered_2020"].sum(), results["biden_2020"].sum(), results["presvotes_2020"].sum(), statewide_bidenpct_2020, results["trump_2020"].sum(), statewide_trumppct_2020]], columns = ['county', 'ballotscast_2020', 'registered_2020', 'turnout_2020', 'biden_2020', 'presvotes_2020', 'bidenpct_2020', 'trump_2020', 'trumppct_2020']).set_index("county")

results.append(statewide).fillna(0).reset_index().rename(columns={'index':'county'}).to_csv("../electionnight/mi/results_2020.csv", index=False)

results_2016 = pd.read_csv("../electionnight/mi/results_2016.csv").set_index("county")
results_2020 = pd.read_csv("../electionnight/mi/results_2020.csv").set_index("county")
results = pd.concat([results_2016, results_2020], axis=1)
results = results.astype({"ballotscast_2020":int,"registered_2020":int,"turnout_2020":float,"biden_2020":int,"presvotes_2020":int,"bidenpct_2020":float,"trump_2020":int,"trumppct_2020":float})

results.to_csv("../electionnight/mi/results.csv")
