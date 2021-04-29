#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os


READ_DIR = '../CSVs'


def get_pattern(l):
    sep = '-'
    if l[-1].startswith('namss.'):
        return ''
    if l[-2].startswith('namss.'):
        return l[-1].lower() 
    pattern = get_pattern(l[:-1])
    return pattern + sep + l[-1].lower()


def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [row for row in reader]
    return csvrows


def main():
    files = [f for f in os.listdir(READ_DIR) if f.endswith('.csv')]
    files.sort()

    patterns = set() 
    for fname in files:
        csvrows = read_csv(os.path.join(READ_DIR, fname))
        try:
            for link, _ in csvrows:
                pattern = get_pattern(link.split('/')[:-1])
                patterns.add(pattern)
        except:
            print("Error:", fname)
            print()

    patterns = list(patterns)
    patterns.sort()
    print(*patterns, sep='\n')


if __name__ == '__main__':
    main()
