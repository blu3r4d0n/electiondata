#!/bin/bash
curl 'https://www.electionreturns.pa.gov/api/Reports/GenerateReport' -H 'Content-Type: application/json' --data-binary '{"ElectionID":83,"ElectionsubType":"G","OfficeIds":[1],"RetOfficeIds":[],"PartyIds":[3,1,4,5,6,13,85,86],"DistrictIds":[],"CandidateIds":[18021,18052,18928,18938,18031,18046,18939,18923,18024,18940,18927,18053,17862,17810,17961,18253,17704,17803,17775,17807,17847,18238,17598,18304,18758,18806,18516,17938,17570,17962,17866,18536,18734,18026,18125,18110,17893,18325,17604,18202,17624,18096,17939,17660,18514,18533,18049,18607,17641,18138,18827,17699,18298,18540,18825,17778,17729,18203,17909,18039,18250,18774,17687,17548,17705,18383,18210,17937,18613,17689,18285,17845,17701,17692,17898,18044,18080,18539,18754,18235,17864,18722,17974,18551,17528,18530,18528,17900,18068,17691,17690,17678,18846,18543,18038,17889,18107,18919,18935,18934,18161,18526,18956,18191,18844,17732,18168,17636,18160,17996,17963,18947,17586,18920,18252,18303,18509,18933,18071,18768,18557,17911,17713,17534,17612,17816,18259,18032,17711,17537,17806,17544,18780,18190,17799,18549,18066,18821,18147,17776,17599,17683,17868,18529,17600,17970,17923,17629,17637,17610,17545,17574,17541,18393,18036,17702,17648,17614,17908,18043,18471,18156,18599,18025,18142,18957,18035,18144,17698,18547,18184,17693,18587,17617,18948,17836,17786,17655,17656,18105,18104,17797,18182,18524,17990,18095,18921,18785,18311,18051,17625,18727,17950,17680,18164,18030,17611,17927,17782,18292,17606,17851,18300,18086,17657,18327,18140,18374,17622,17965,18620,18474,18949,18312,18360,18950,17731,17834,17871,18961,18648,18102,18294,18706,17608,18510,18118,17567,18245,18155,18251,17808,17613,18476,18958,18042,17647,17902,17934,17677,17715,17632,17812,18239,17527,17664,18878,17890,18347,18013,18186,17679,18208,17642,18955,18192,17886,18512,17969,17758,18165,18729,18204,18925,18396,17910,18001,18588,17529,17547,17627,18133,17654,17891,17784,17885,17901,18922,17760,18172,18207,17914,17578,17919,18954,18124,17989,18307,17618,18608,17658,17650,17971,17532,17639,18959,17999,18343,17820,18195,17935,17920,18029,18637,17964,18791,17863,17895,18257,17925,18004,18019,18114,17839,17595,18952,17975,18937,17929,17546,17773,18834,18085,18122,18960,17576,18120,18356,17915,18129,18916,17688,18012,18094,17762,18183,17572,17697,18507,18188,17594,17941,17739,17757,17903,17694,17673,17675,18522,18254,17536,18034,18169,18689,17956,17573,17792,17749,18175,18158,17998,18574,17634,17531,18040,17703,17638,18232,17918,17759,17681,17620,17781,18930,17643,17917,18682,17922,18301,17892,17967,17672,17585,18796,18593,18246,18151,18320,18189,17944,17607,18845,18255,17676,18134,17623,18778,18366,18131,18713,18336,17761,17842,18240,18272,18011,17644,18145,17628,17986,17789,18651,18936,18953,17619,17733,17571,18197,17972,18917,17706,17575,17621,18137,17973,17905,18261,18150,17795,18149,18966,18788,18098,17663,17777,17873,18009,18444,17958,18964],"CountyIds":[2290,2291,2292,2293,2294,2295,2296,2297,2298,2299,2300,2301,2302,2303,2304,2305,2306,2307,2308,2309,2310,2311,2312,2313,2314,2315,2316,2317,2318,2319,2320,2321,2322,2323,2324,2325,2326,2327,2328,2329,2330,2331,2332,2333,2334,2335,2336,2337,2338,2339,2340,2341,2342,2343,2344,2345,2346,2347,2348,2349,2350,2351,2352,2353,2354,2355,2356],"ReferendumIds":[],"ReferendumDetailIds":[],"ExportType":"T","ReportType":"C","FileName":"UnOfficial"}' --compressed  > ../electionnight/pa/live_results.csv 

newfile='../electionnight/pa/live_results.csv'
oldfile='../electionnight/pa/olddata.csv'

cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python make_pa.py
var="pa_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/pa/* && git commit -m $var && git push)
fi

