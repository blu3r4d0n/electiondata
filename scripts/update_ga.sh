#!/bin/bash
wget -q -O ../electionnight/ga/detailxls.zip https://results.enr.clarityelections.com//GA//105369/265407/reports/detailxls.zip
unzip -o ../electionnight/ga/detailxls.zip -d ../electionnight/ga/
mv ../electionnight/ga/detail.xls ../electionnight/ga/live_results.xls
rm ../electionnight/ga/detailxls.zip 

libreoffice --headless --convert-to xlsx ../electionnight/mi/live_results.xls --outdir ../electionnight/ga/ 
newfile='../electionnight/ga/live_results.xlsx'
oldfile='../electionnight/ga/olddata.xlsx'
cmp --silent $newfile $oldfile || changed=true
if [ $changed ];
then 
python make_ga.py
cp ../electionnight/ga/live_results.xlsx ../electionnight/ga/olddata.xlsx
var="ga_$(date '+%Y-%m-%dT%H:%M')"
(git add ../electionnight/ga/* && git commit -m $var && git push)
fi
