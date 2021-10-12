#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import traceback

from tqdm import tqdm


SURVEYS_DIR = '../Migrated_Files'
HEADERS_DIR = '../Meshed_Survey_Headers'


def get_textual_header(segy_file):
    with open(segy_file, 'rb') as f:
        textual_header = f.read(3200)

    encoding = 'cp500'
    if textual_header.isascii():
        encoding = 'utf-8'
    textual_header = textual_header.decode(encoding)
    textual_header = ["{:02d} {}".format(i//80+1, textual_header[i:i+80])
            for i in range(0, len(textual_header), 80)]
        
    return textual_header


def mesh_headers(survey_dir):
    segy_files = os.listdir(survey_dir)
    segy_files.sort()

    all_headers = list()
    for segy_file in segy_files:
        segy_path = os.path.join(survey_dir, segy_file)
        all_headers += get_textual_header(segy_path)

    meshed_headers = set(all_headers)
    meshed_headers = list(meshed_headers)
    meshed_headers.sort()
    meshed_headers = "\n".join(meshed_headers) 
    
    return meshed_headers


def main():
    # Create directories and log files
    os.makedirs(HEADERS_DIR, exist_ok=True)

    surveys = os.listdir(SURVEYS_DIR)
    surveys.sort()

    print("Meshing headers from", len(surveys), "surveys.")
    print()
    time.sleep(1)

    bar = tqdm(surveys)
    for survey in bar:
        bar.set_description(survey, refresh=True)

        segy_dir_path = os.path.join(SURVEYS_DIR, survey)
        header_path = os.path.join(HEADERS_DIR, survey + '.txt')

        meshed_headers = mesh_headers(segy_dir_path)

        with open(header_path, 'w') as f:
            f.write(meshed_headers)


if __name__ == '__main__':
    main()
