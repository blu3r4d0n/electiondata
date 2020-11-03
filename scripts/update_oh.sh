#!/bin/bash
wget -q -O ../electionnight/oh/live_results.xlsx https://liveresults.ohiosos.gov/Api/v1/download\?filename\=GeneralElectionXlsFile
newfile='../electionnight/oh/live_results.xlsx'
oldfile='../electionnight/oh/olddata.xlsx'

cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python make_oh.py
cp ../electionnight/oh/live_results.xlsx ../electionnight/oh/olddata.xlx
var="oh_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/oh/* && git commit -m $var && git push)
fi

