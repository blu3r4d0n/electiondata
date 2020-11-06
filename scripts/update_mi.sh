#!/bin/bash
wget -q -O ../electionnight/mi/live_results.xls https://mielections.us/election/results/DATA/2020GEN_MI_CENR_BY_COUNTY.xls
libreoffice --headless --convert-to csv ../electionnight/mi/live_results.xls --outdir ../electionnight/mi/ 
newfile='../electionnight/mi/live_results.csv'
oldfile='../electionnight/mi/olddata.csv'
rm ../electionnight/mi/live_results.xls
cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python3 make_mi.py
cp ../electionnight/mi/live_results.csv ../electionnight/mi/olddata.csv
var="mi_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/mi/* && git commit -m $var && git push)
fi

