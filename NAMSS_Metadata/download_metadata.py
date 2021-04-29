#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os
import requests
import traceback

from bs4 import BeautifulSoup
from urllib import parse
from time import sleep
from tqdm import tqdm
from xml.etree import ElementTree as ET

# CSV Info
CSV_FILE = './2DSeismic.csv'
SURVEY_COLUMN = 0
LINK_COLUMN = 7

# Save options
SAVE_DIR = '2DSeismic_json'
ERR_FILE = './logs/faulty_links_2021-04-13.log'

# Creates save and log directories, if necessary
logdir = os.path.dirname(ERR_FILE)
if logdir:
    os.makedirs(logdir, exist_ok=True)
os.makedirs(SAVE_DIR, exist_ok=True)

# Starts global session
session = requests.Session()
session.auth = ('user', 'pass')


def get_dataset_info(url):
    page = session.get(url, timeout=2, stream=True)

    soup = BeautifulSoup(page.content, 'html.parser')

    info = {}
    fsize_tag = soup.find_all("span", class_='filesize')[0]
    fsize = fsize_tag.text.strip('()').replace('\xa0', ' ') 
    info['datasetSize'] = fsize 

    info['datasetZipLink'] = soup.find_all('a', text='Download')[0]['href']
    info['datasetContentLink'] = url + 'dataset/'

    return info


# Recursively process XML
def process_xml(element):
    # Base case
    if element.text == None:
        return None
    elif element.text.strip('\n\t'):
        return element.text

    d = {}
    for e in element:
        child = process_xml(e)
        if child is None:
            continue
        if e.tag in d:
            if type(child) == dict:
                d[e.tag].update(child)
            else: 
                d[e.tag] += (', ' + child)
        else:
            d[e.tag] = child

    return d


def downlod_xml(xml_link):
    page = session.get(xml_link, timeout=2, stream=True)
    xml_file = page.headers['Content-Disposition'].split()[1].split('=')[1].strip('"')
    xml = page.content

    return xml, xml_file


# Assumes a tab-separated CSV file, generated with the 'combine_CSVs.py' script
# First line are column headers.
def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [row for row in reader]

    # Construct a dictionary mapping a survey to it's link
    survey_links = dict()
    for line in csvrows[1:]:
        survey_name = line[SURVEY_COLUMN].replace(' ', '-').lower()
        link = line[LINK_COLUMN]
        survey_links[survey_name] = link

    return survey_links


def process_link(link):
    xml_link = link + 'metadata/seismic/download/'
    xml, xml_file = downlod_xml(xml_link)
    root = ET.fromstring(xml)

    xml_dict = {}
    for e in root:
        child = process_xml(e)
        if e.tag in xml_dict:
            xml_dict[e.tag].update(child)
        else:
            xml_dict[e.tag] = child

    xml_dict['datasetInformation'].update(get_dataset_info(link))

    return xml_dict


def save_json(json_file, xml):
    with open(json_file, 'w') as f:
        json.dump(xml, f)


def main():
    surveys = read_csv(CSV_FILE)

    bar = tqdm(surveys, leave=True)
    downloaded = 0
    errors = 0
    for s in bar:
        fname = os.path.join(SAVE_DIR, s) + '.json'
        bar.set_description("Downloading {}".format(s), refresh=True)
        # If the file already exists, skips download
        if os.path.exists(fname):
            continue

        try:
            link = surveys[s]
            xml = process_link(link)
            save_json(fname, xml)
            downloaded += 1
            sleep(1)
        except Exception as e:
            errors += 1
            err_msg = "Error in survey " + s + ':\n'
            err_msg += traceback.format_exc() + '\n'
            with open(ERR_FILE, 'a') as f:
                f.write(err_msg)

    print(downloaded, "files downloaded.")
    if errors:
        print(errors, "errors found.")
        print("See", ERR_FILE, "for details.")

if __name__ == '__main__':
    main()
