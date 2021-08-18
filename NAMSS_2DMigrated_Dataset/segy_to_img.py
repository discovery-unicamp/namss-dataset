#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import time
import traceback

from aux import read_segy
from imageio import imsave
from tqdm import tqdm


# Choose png, jpg or tiff
IMG_FORMAT = 'png'

SURVEYS_DIR = 'Migrated_Files'
IMG_DIR = 'Migrated_PNG'
LOG_DIR = 'logs'


def save_segy_as_img(segy_file, img_file):
    img_format = os.path.splitext(img_file)[1].strip('.')
    if img_format in ['png', 'jpg']:
        drange = [0, 255]
        dtype = np.uint8
    elif img_format == 'tiff':
        drange = [-1., 1.]
        dtype = np.float32
    else:
        raise RuntimeError("Cannot save data as image format " + img_format)
    data = read_segy.read_seismic_data(segy_file)
    data = read_segy.normalize(data, drange, dtype)
    
    imsave(img_file, data)

    return


def log_status(log_file, fpath, status):
    with open(log_file, 'a') as log:
        print(fpath, status, sep='\t', file=log)


def main():
    # Create directories and log files
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = time.strftime('%Y-%m-%d_%Hh%Mm', time.localtime()) 
    err_file = os.path.join(LOG_DIR, IMG_FORMAT + '_errors_' + timestamp + '.log')
    log_file = os.path.join(LOG_DIR, IMG_FORMAT + '_' + timestamp + '.log')

    surveys = os.listdir(SURVEYS_DIR)
    surveys.sort()

    print("Converting", len(surveys), "surveys to", IMG_FORMAT.upper(), "image format.")
    print()
    time.sleep(2)

    converted_data = 0
    errors = 0
    for i, survey in enumerate(surveys):
        img_dir_path = os.path.join(IMG_DIR, survey)
        os.makedirs(img_dir_path, exist_ok=True)

        segy_dir_path = os.path.join(SURVEYS_DIR, survey)
        segy_files = os.listdir(segy_dir_path)
        segy_files.sort()

        bar = tqdm(segy_files)
        bar.set_description("Survey {} ({} of {})".format(survey, i+1, len(surveys)), refresh=True)
        for segy_file in bar:
            segy_path = os.path.join(segy_dir_path, segy_file)
            segy_name = os.path.splitext(segy_file)[0]
            img_path = os.path.join(img_dir_path, segy_name + '.' + IMG_FORMAT)
            if os.path.exists(img_path):
                log_status(log_file, segy_path, 'ALREADY CONVERTED')
                continue
            try:
                save_segy_as_img(segy_path, img_path)
                log_status(log_file, segy_path, 'PASS')
                converted_data += 1
                    
            except Exception as e:
                err_msg = "Error in file " + segy_path + '\n'
                err_msg += traceback.format_exc() + '\n'
                with open(err_file, 'a') as f:
                    f.write(err_msg)
                log_status(log_file, segy_path, 'FAIL')
                errors += 1

    print()
    if errors:
        print(errors, "errors occurred.")
        print("View", err_file, "for details.")
    if converted_data:
        print(converted_data, "data converted to", IMG_FORMAT, 'format.')
        print("View", log_file, "for details.")


if __name__ == '__main__':
    main()
