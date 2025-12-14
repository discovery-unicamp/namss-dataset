#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import dataset_info

from imageio import imsave, imread
from multiprocessing import Pool
from time import time
from tqdm import tqdm


SOURCE_DIR = './Migrated_TIFF'
TARGET_DIR = '../Data/NAMSS/NAMSS_{}_HR'

DIVISIBLE_BY = 12
SMALLEST_IMG_SIZE = 192
MAX_IMG_WIDTH = 2000
N_PROC = os.cpu_count() 


def discard_line(fpath, survey):
    discarded_lines = dataset_info.get_discarded_lines()
    line = os.path.splitext(fpath)[0]
    if line in discarded_lines.get(survey, set()):
        return True
    return False


print("\nThis script will read TIFF images from ", SOURCE_DIR, ", disregarding files which are in the discarded list, crop the images, and save them to ", TARGET_DIR.format("{train/valid/test}"), ".\n", sep='')

input("Press any key to continue or Ctrl+C to abort.")
print()

start_time = time()
split = dataset_info.get_survey_split()
surveys = os.listdir(SOURCE_DIR)
surveys.sort()
for i, survey in enumerate(surveys, start=1):
    split_set = split[survey]
    if split_set == 'discarded':
        continue

    read_dir = os.path.join(SOURCE_DIR, survey)
    fnames = os.listdir(read_dir)
    fnames = [f for f in fnames if not discard_line(f, survey)]
    if len(fnames) == 0:
        continue

    save_dir = TARGET_DIR.format(split_set)
    os.makedirs(save_dir, exist_ok=True)
    target_fname = survey + ".{}"
    target_fpath = os.path.join(save_dir, target_fname)

    def crop_and_save_img(fname):
        read_path = os.path.join(read_dir, fname)

        img = imread(read_path)
        # Clears TIFF metadata
        img.meta.clear()

        row_begin = (img.shape[0] % DIVISIBLE_BY) // 2
        row_end = row_begin + (img.shape[0] // DIVISIBLE_BY) * DIVISIBLE_BY
        col_begin = (img.shape[1] % DIVISIBLE_BY) // 2
        col_end = col_begin + (img.shape[1] // DIVISIBLE_BY) * DIVISIBLE_BY
        new_height = row_end - row_begin
        new_width = col_end - col_begin

        if new_height >= SMALLEST_IMG_SIZE and new_width >= SMALLEST_IMG_SIZE:
            img = img[row_begin:row_end, col_begin:col_end]
            if new_width <= MAX_IMG_WIDTH:
                save_path = target_fpath.format(fname)
                imsave(save_path, img)
            # Break up big images into sub images,
            # keeping each sub image width divisible by 'DIVISIBLE_BY'
            else:
                num_sub_imgs = new_width // MAX_IMG_WIDTH + 1
                sub_width = new_width // num_sub_imgs
                sub_width -= (sub_width % DIVISIBLE_BY)
                part = ".part{:02d}"
                fname = os.path.splitext(fname)[0] + part + os.path.splitext(fname)[1]
                for i in range(num_sub_imgs - 1):
                    begin = i * sub_width
                    end = (i+1) * sub_width
                    sub_img = img[:,begin:end]
                    save_path = target_fpath.format(fname.format(i+1))
                    imsave(save_path, sub_img)
                # Last sub image might have a bigger size then the other parts
                begin = (num_sub_imgs - 1) * sub_width
                sub_img = img[:,begin:]
                save_path = target_fpath.format(fname.format(num_sub_imgs))
                imsave(save_path, sub_img)

    with Pool(N_PROC) as p:
        bar = tqdm(p.imap(crop_and_save_img, fnames), total=len(fnames))
        bar.set_description("Survey {} ({} of {})".format(survey, i, len(surveys)), refresh=True)
        # List is necessary to make tqdm iterate
        list(bar)

print("\nTempo para conversão: {:.3f}s\n".format(time()-start_time))
