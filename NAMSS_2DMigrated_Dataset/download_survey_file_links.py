#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import requests
import time
import traceback

from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm


LINKS_FILE = './survey_dataset_links.csv'
SAVE_DIR = 'CSVs'
LOG_DIR = 'logs'
TIMEOUT = 5


# Create directories and log files
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

timestamp = time.strftime('%Y-%m-%d_%Hh%Mm', time.localtime()) 
err_file = os.path.join(LOG_DIR, 'errors_' + timestamp + '.log')
log_file = os.path.join(LOG_DIR, 'downloads_' + timestamp + '.log')

# Starts HTTP session
session = requests.Session()
session.auth = ('user', 'pass')

def get_data_info(url):
    page = session.get(url, timeout=TIMEOUT, stream=True)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', class_='table table-striped')[0]
    tbody = table.find_all('tbody')[0]
    rows = tbody.find_all('tr')

    info = []
    for row in rows:
        link, fsize, _ = [c for c in row if c.name == 'td']
        link = link.find_all('a')
        if not link:
            continue

        link = link[0]['href']
        value, unit = fsize.contents[0].split('\xa0')
        value = float(value)
        # Convert value to Mega Byte
        if unit == 'GB': value *= 10**3 
        elif unit == 'KB': value *= 10**-3 
        elif unit == 'bytes': value *= 10**-6 

        info.append([link, value])

    return info


def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [row for row in reader]
    # Adjust survey names
    for row in csvrows:
        row[0] = row[0].replace(' ', '-').lower()
    return csvrows


def write_csv(csvfile, rows):
    with open(csvfile, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerows(rows) 


def log_status(log_file, survey, status):
    with open(log_file, 'a') as log:
        print(survey, status, sep='\t', file=log)


def main():
    survey_links = read_csv(LINKS_FILE)

    downloads = 0
    errors = 0
    bar = tqdm(survey_links, leave=True)
    for survey, link in bar:
        bar.set_description("Downloading survey {}".format(survey), refresh=True)

        # If the file already exists, skips download
        csvfile = os.path.join(SAVE_DIR, survey + '.csv')
        if os.path.exists(csvfile):
            log_status(log_file, survey, 'ALREADY DOWNLOADED')
            continue

        try:
            info = get_data_info(link)
            write_csv(csvfile, info)
            log_status(log_file, survey, 'PASS')
            downloads += 1
            sleep(1)
                
        except Exception as e:
            err_msg = "Error in link " + link + '\n'
            err_msg += traceback.format_exc() + '\n'
            with open(err_file, 'a') as f:
                f.write(err_msg)
            log_status(log_file, survey, 'FAIL')
            errors += 1

    if errors:
        print(errors, "errors occurred.")
        print("View", err_file, "for details.")
    if downloads:
        print(downloads, "survey data links downloaded.")
        print("View", log_file, "for details.")


if __name__ == '__main__':
    main()
