#!/bin/bash

function build_json_files {
  for file in $(ls *.csv)
  do 
    ./csv2json.rb $file
  done
}

#assumes one follows these steps
#https://gist.github.com/CristinaSolana/1885435
function sync_with_original_repo {
  git fetch upstream
  git pull upstream master
  build_json_files
  git add .
  git commit -m "$(date)"
  git push origin json
}

#now run this in cron periodically
sync_with_original_repo
