#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os

CSVFILE = './2DSeismic_all_metadata.csv'
JSON_DIR = './2DSeismic_json'


def merge_data(data, name):
    if not type(data) == dict:
        return {name : data.replace('\n', ' ').replace('\t', '    ')}

    d = {}
    for k in data:
        d.update(merge_data(data[k], name + '.' + k))

    return d


def get_files(JSON_DIR):
    files = os.listdir(JSON_DIR)
    files.sort()
    files = [os.path.join(JSON_DIR, f) for f in files]
    return files


def process_file(fname):
    with open(fname) as f:
        metadata = json.load(f)

    d = {}
    for k in metadata:
        d.update(merge_data(metadata[k], k))

    return d


def main():
    fnames = get_files(JSON_DIR)

    all_data = []
    for f in fnames:
        all_data.append(process_file(f))

    fieldnames = []
    for d in all_data:
        fieldnames += d.keys()
    fieldnames = list(set(fieldnames))
    fieldnames.sort()

    with open(CSVFILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for d in all_data:
            writer.writerow(d)


if __name__ == '__main__':
    main()
