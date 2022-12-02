#!/bin/bash

subj=$1
mkdir ../finalobjects/$subj

paste -- "files.txt" "labels.txt" |
while IFS=$'\t' read -r file1 file2 rest; do
  
  echo "$file1 $file2"
  cp ../objects/$subj/$file1  ../finalobjects/$subj/$file2.obj
done
