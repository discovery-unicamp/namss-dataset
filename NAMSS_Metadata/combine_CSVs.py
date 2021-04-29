#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Combine collected CSV files from https://walrus.wr.usgs.gov/namss/search/
# into a single file, with tab (\t) separator, removing duplicate lines.

import csv
import os

CSVDIR = './Collected_CSVs'
SAVEFILE = './2DSeismic.csv'

# Assumes first line is the NAMSS query link and
# second line the CSV column headers.
def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f)
        csvrows = [row for row in reader]
    header = csvrows[1]
    rows = csvrows[2:]
    return header, rows


def write_csv(csvfile, header, rows):
    with open(csvfile, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerow(header) 
        csv_writer.writerows(rows) 


def main():
    csvfiles = [os.path.join(CSVDIR, f) for f in os.listdir(CSVDIR) if f.endswith('.csv')]

    all_rows = []
    for csv in csvfiles:
        header, rows = read_csv(csv)
        for r in rows:
            # Only add new rows
            if not r in all_rows:
                all_rows.append(r)

    # Sort by Survey name and save
    all_rows.sort(key=lambda row: row[0])
    write_csv(SAVEFILE, header, all_rows)


if __name__ == '__main__':
    main()
