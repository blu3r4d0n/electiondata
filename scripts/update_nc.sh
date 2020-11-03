#!/bin/bash
wget -q -O ../electionnight/nc/results_pct_20201103.zip https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/results_pct_20201103.zip
unzip -o ../electionnight/nc/results_pct_20201103.zip -d ../electionnight/nc/
mv ../electionnight/nc/results_pct_20201103.txt ../electionnight/nc/live_results.txt
rm ../electionnight/nc/results_pct_20201103.zip 

newfile='../electionnight/nc/live_results.txt'
oldfile='../electionnight/nc/olddata.txt'

cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python make_nc.py
cp ../electionnight/nc/live_results.txt ../electionnight/nc/olddata.txt
var="nc_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/nc/* && git commit -m $var && git push)
fi

