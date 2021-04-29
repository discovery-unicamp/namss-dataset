#!/bin/bash

CSV_DIR=./Migrated_Balanced
SAVE_DIR=./Migrated_Files

# Set Internal File Separator to newline only
OLD_IFS=$IFS
IFS=$'\n'

for FILE in `ls $CSV_DIR` ; do
    echo "Downloading links from $FILE" ;
    dirname=`echo "$FILE" | sed 's/\.csv//'`
    mkdir -p "$SAVE_DIR/$dirname"

    URLS=`cut $CSV_DIR/$FILE -f1`
    for url in $URLS ; do
        fname=`echo ${url} | sed 's/.*\///'`
        fpath="$SAVE_DIR/$dirname/$fname"
        url=`echo ${url} | sed 's/ /%20/g'`

        if test -f "$fpath" ; then
            echo -e "$fpath\tDOWNLOADED" ;
            continue
        fi

        status=$(curl -s -f -w %{http_code} "$url" -o "$fpath") ;
        if [ $status -ne 200 ] ; then
            echo -e "$fpath\tFAIL ($status)" ;
        else
            echo -e "$fpath\tSUCCESS" ;
        fi
    done 
    echo ""; 
done

# Reset standard IFS
IFS=$OLD_IFS
