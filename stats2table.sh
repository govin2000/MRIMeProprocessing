#!/bin/bash

sub_id=$1
echo $sub_id

export SUBJECTS_DIR='../FreeSurfer'
output='../FreeSurferData'
asegstats2table --subjects $sub_id --meas volume --tablefile $output/$sub_id'_aseg.txt'
aparcstats2table --subjects $sub_id --meas volume --hemi rh --tablefile $output/$sub_id'_rh_aparc.txt'
aparcstats2table --subjects $sub_id --meas volume --hemi lh --tablefile $output/$sub_id'_lh_aparc.txt'


