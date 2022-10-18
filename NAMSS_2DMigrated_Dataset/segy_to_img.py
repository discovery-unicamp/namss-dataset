#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import time
import traceback

from aux import read_segy
from functools import lru_cache
from imageio import imsave
from pathlib import Path
from tqdm import tqdm


# Choose png, jpg or tiff
IMG_FORMAT = 'tiff'

SURVEYS_DIR = 'Migrated_Files'
IMG_DIR = 'Migrated_' + IMG_FORMAT.upper()
LOG_DIR = 'logs'

@lru_cache(maxsize=None)
def get_exceptions():
    duplicate_surveys = \
    """w-5-77-ar
    w-8-78-ar
    w-17-77-ar
    w-18-77-ar
    w-19-78-ar
    w-62-77-ar""".split('\n')
    duplicate_surveys = [d.strip() for d in duplicate_surveys] 

    corrupted_lines_raw = \
    """b-10-82-at/G82-139_migr.segy
    b-15-77-ak/SP77-004_2__SP-9.sgy
    b-15-77-ak/SP77-014__SP-3.sgy
    b-15-77-ak/SP77-016_2__SP-7.sgy
    b-15-77-ak/SP77-017_1__SP-7.sgy
    b-15-77-ak/SP77-025__SP-4.sgy
    b-15-77-ak/SP77-028_1__SP-8.sgy
    b-15-77-ak/SP77-037__SP-11.sgy
    b-15-77-ak/SP77-047__SP-5.sgy
    b-15-77-ak/SP77-055__SP-5.sgy
    b-15-77-ak/SP77-057__SP-5.sgy
    b-15-77-ak/SP77-088__SP-6.sgy
    b-15-77-ak/SP77-090__SP-6.sgy
    b-15-77-ak/SP77-096__SP-10.sgy
    h-17-79-sc/4331__7-12127.1.sgy
    h-17-79-sc/4509__7-12105.1.sgy
    l-4-90-sc/l4mig118.sgy
    w-40-80-ak/EP-31.sgy
    w-6-85-sc/SB85-10_501151.sgy
    w-6-85-sc/SB85-12_501151.sgy
    w-6-85-sc/SB85-13_501151.sgy
    w-6-85-sc/SB85-16_500968.sgy
    w-6-85-sc/SB85-17_500968.sgy
    w-6-85-sc/SB85-18_500968.sgy
    w-6-85-sc/SB85-19_500968.sgy
    w-6-85-sc/SB85-20_500968.sgy
    w-6-85-sc/SB85-21_500968.sgy
    w-6-85-sc/SB85-23_500968.sgy
    w-6-85-sc/SB85-24_500968.sgy
    w-6-85-sc/SB85-28_501421.sgy
    w-6-85-sc/SB85-29_501421.sgy
    w-6-85-sc/SB85-33_501421.sgy
    w-6-85-sc/SB85-35_501421.sgy
    w-6-85-sc/SB85-36_501421.sgy
    w-6-85-sc/SB85-37_501421.sgy
    w-6-85-sc/SB85-39_501421.sgy
    w-6-85-sc/SB85-40_501421.sgy
    w-18-75-np/WR-001_3_4__245335.sgy
    w-18-75-np/WR-001__596180.sgy
    w-18-75-np/WR-001A_1__220158.sgy
    w-18-75-np/WR-001A_2__206209.sgy
    w-18-75-np/WR-001A_3__249999.sgy
    w-18-75-np/WR-001A_3__252047.sgy
    w-18-75-np/WR-001A_4_5__236463.sgy
    w-18-75-np/WR-001A_4_5__586070.sgy
    w-18-75-np/WR-004__574766.sgy
    w-18-75-np/WR-006__413580.sgy
    w-18-75-np/WR-008__116150.sgy
    w-18-75-np/WR-010__245369.sgy
    w-18-75-np/WR-010__419990.sgy
    w-18-75-np/WR-012__247817.sgy
    w-18-75-np/WR-014__531897.sgy
    w-18-75-np/WR-016__123039.sgy
    w-18-75-np/WR-018__589294.sgy
    w-18-75-np/WR-018__591987.sgy
    w-18-75-np/WR-022__325434.sgy
    w-18-75-np/WR-024__406294.sgy
    w-18-75-np/WR-024__555526.sgy
    w-18-75-np/WR-026__593971.sgy""".split('\n')

    corrupted_lines = dict()
    for line in corrupted_lines_raw:
        survey, line = line.strip().split('/')
        if survey not in corrupted_lines:
            corrupted_lines[survey] = [line]
        else:
            corrupted_lines[survey].append(line)

    return duplicate_surveys, corrupted_lines


def discard_segy(segy_file):
    duplicate_surveys, corrupted_lines = get_exceptions()
    survey, linefile = Path(segy_file).parts[-2:]
    if survey in duplicate_surveys:
        return True
    if survey in corrupted_lines and linefile in corrupted_lines[survey]:
        return True
    with open(segy_file, 'rb') as f:
        dt = read_segy.read_field(f, 3217)
    if dt != 4000:
        return True

    return False


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
                if discard_segy(segy_path):
                    log_status(log_file, segy_path, 'DISCARDED')
                    continue
                else:
                    save_segy_as_img(segy_path, img_path)
                    log_status(log_file, segy_path, 'SAVED')
                    converted_data += 1
                    
            except Exception as e:
                err_msg = "Error in file " + segy_path + '\n'
                err_msg += traceback.format_exc() + '\n'
                with open(err_file, 'a') as f:
                    f.write(err_msg)
                log_status(log_file, segy_path, 'FAIL')
                errors += 1

        # If img survey dir is empty (no files saved), erase it
        if not list(os.scandir(img_dir_path)):
            os.rmdir(img_dir_path)

    print()
    if errors:
        print(errors, "errors occurred.")
        print("View", err_file, "for details.")
    if converted_data:
        print(converted_data, "data converted to", IMG_FORMAT, 'format.')
        print("View", log_file, "for details.")


if __name__ == '__main__':
    main()
