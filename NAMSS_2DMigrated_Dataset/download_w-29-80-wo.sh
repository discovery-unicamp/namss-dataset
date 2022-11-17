#!/bin/bash

# Survey W-29-80-WO direct file links are broken
# So manually download the full dataset and extract the selected files

CSV_DIR=./Migrated_Balanced
SAVE_DIR=./Migrated_Files

# Set Internal File Separator to newline only
OLD_IFS=$IFS
IFS=$'\n'
csv_file=w-29-80-wo.csv
dirname=`echo "$csv_file" | sed 's/\.csv//'`
dirpath=$SAVE_DIR/$dirname

# Check if files already exist
if [ "$(ls -A $dirpath)" ]; then
	echo "Directory $dirpath is not empty:" ;
	echo "" ;
	find $dirpath -type f ; 
	echo "" ;
	echo "Exiting.";
	exit ;
fi

# Download ZIP file
mkdir -p tmp ;
wget -P tmp --no-clobber https://walrus.wr.usgs.gov/namss/data/1980/namss.W-29-80-WO.mcs.airgun.zip ;

# Extract only selected migrated files
URLS=`cut $CSV_DIR/$csv_file -f1`
for url in $URLS ; do
	fname=`echo ${url} | sed 's/.*\///'`
	zipfpath="Data/SEGY/Migration/$fname"
	unzip -nj tmp/namss.W-29-80-WO.mcs.airgun.zip $zipfpath -d $dirpath ;
done

echo "" ;
echo "If all went well, consider cleaning up by removing ./tmp directory."
echo "" ;

# Reset standard IFS
IFS=$OLD_IFS

