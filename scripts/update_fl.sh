#!/bin/bash
wget -q -O ../electionnight/fl/live_results.txt https://flelectionfiles.floridados.gov/enightfilespublic/20201103_ElecResultsFL.txt
newfile='../electionnight/fl/live_results.txt'
oldfile='../electionnight/fl/olddata.txt'

cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python3 make_fl.py
cp ../electionnight/fl/live_results.txt ../electionnight/fl/olddata.txt
var="fl_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/fl/* && git commit -m $var && git push)
fi

