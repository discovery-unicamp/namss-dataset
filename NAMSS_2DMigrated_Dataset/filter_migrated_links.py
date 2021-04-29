#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os


READ_DIR = 'CSVs'
WRITE_DIR = 'Migrated_CSV'


accepted_patterns = [
    'data',
    'data-segy-depth',
    'data-segy-migration',
    'data-segy-reprocessed',
    'segy-area17_migrated',
    'segy-area18_migrated',
    'segy-area19_migrated',
    'segy-area5_migrated',
    'segy-area8_migrated',
    'segy-mig',
    'segy-migrated'
    ]

def get_pattern(l):
    sep = '-'
    if l[-1].startswith('namss.'):
        return ''
    if l[-2].startswith('namss.'):
        return l[-1].lower() 
    pattern = get_pattern(l[:-1])
    return pattern + sep + l[-1].lower()


def is_migrated_data(link):
    if not (link.endswith('segy') or link.endswith('sgy')):
        return False
    pattern = get_pattern(link.split('/')[:-1])
    if pattern in accepted_patterns:
        return True
    else:
        return False


def filter_migrated_links(csvrows):
    filtered_rows = []
    for link, value in csvrows:
        if is_migrated_data(link):
            filtered_rows.append([link, value])
    return filtered_rows


def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [row for row in reader]
    return csvrows


def write_csv(csvfile, csvrows):
    with open(csvfile, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerows(csvrows) 


def main():
    os.makedirs(WRITE_DIR, exist_ok=True)

    files = os.listdir(READ_DIR)
    files.sort()

    no_patterns = []
    saved = 0
    for fname in files:
        csvrows = read_csv(os.path.join(READ_DIR, fname))
        csvrows = filter_migrated_links(csvrows)
        if not csvrows:
            no_patterns.append(fname)
        else:
            write_csv(os.path.join(WRITE_DIR, fname), csvrows)
            saved += 1

    print(saved, "files saved in", WRITE_DIR)
    if no_patterns:
        print("The files\n")
        print(*no_patterns, '', sep='\n')
        print("had no links with the accepted patterns.")


if __name__ == '__main__':
    main()
