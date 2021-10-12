#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import traceback

from tqdm import tqdm


SURVEYS_DIR = '../Migrated_Files'
HEADERS_DIR = '../Survey_Headers'


def get_textual_header(segy_file):
    with open(segy_file, 'rb') as f:
        textual_header = f.read(3200)

    encoding = 'cp500'
    if textual_header.isascii():
        encoding = 'utf-8'
    textual_header = textual_header.decode(encoding)
    textual_header = [textual_header[i:i+80] for i in range(0, len(textual_header), 80)]
    textual_header = "\n".join(textual_header) 
        
    return textual_header


def main():
    # Create directories and log files
    os.makedirs(HEADERS_DIR, exist_ok=True)

    surveys = os.listdir(SURVEYS_DIR)
    surveys.sort()

    print("Extracting headers from", len(surveys), "surveys.")
    print()
    time.sleep(1)

    bar = tqdm(surveys)
    for survey in bar:
        bar.set_description(survey, refresh=True)
        header_dir_path = os.path.join(HEADERS_DIR, survey)
        os.makedirs(header_dir_path, exist_ok=True)

        segy_dir_path = os.path.join(SURVEYS_DIR, survey)
        segy_files = os.listdir(segy_dir_path)
        segy_files.sort()

        for segy_file in segy_files:
            segy_path = os.path.join(segy_dir_path, segy_file)
            segy_name = os.path.splitext(segy_file)[0]
            header_path = os.path.join(header_dir_path, segy_name + '.txt')

            textual_header = get_textual_header(segy_path)
            with open(header_path, 'w') as f:
                f.write(textual_header)


if __name__ == '__main__':
    main()
