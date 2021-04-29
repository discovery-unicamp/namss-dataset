#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import random


# Set max survey size in MB
MAX_SURVEY_SIZE = 300

# Set seed to repeat a particular draw
SEED = None
#SEED = 15768300955983471839

MIGRATED_DIR = './Migrated_CSV'
BALANCED_DIR = './Migrated_Balanced'


# Set and save seed
LOGS_DIR = 'logs'
SEED_LOG = os.path.join(LOGS_DIR, 'seeds.log')
if not SEED:
    SEED = int.from_bytes(os.urandom(8), 'big')
random.seed(SEED)
now = datetime.datetime.now()
os.makedirs(LOGS_DIR, exist_ok=True)
with open(SEED_LOG, 'a') as f:
    line = "Balance Survey. Date: {}, seed: {}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), SEED)
    f.write(line)


def balance_survey(survey_links, max_size):
    # Keep only files that fits max_size
    survey_links = [rows for rows in survey_links if rows[1] <= max_size]

    if not survey_links:
        return []

    ind = random.randint(0, len(survey_links)-1)
    selected_element = survey_links.pop(ind)
    max_size -= selected_element[1]

    return [selected_element] + balance_survey(survey_links, max_size)


def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [[row[0], float(row[1])] for row in reader]
    return csvrows


def write_csv(csvfile, csvrows):
    with open(csvfile, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerows(csvrows) 


def main():
    os.makedirs(BALANCED_DIR, exist_ok=True)

    files = os.listdir(MIGRATED_DIR)
    files.sort()

    for fname in files:
        survey_links = read_csv(os.path.join(MIGRATED_DIR, fname))
        selected_links = balance_survey(survey_links, MAX_SURVEY_SIZE)
        selected_links.sort(key=lambda s: s[0])
        write_csv(os.path.join(BALANCED_DIR, fname), selected_links)

if __name__ == '__main__':
    main()
