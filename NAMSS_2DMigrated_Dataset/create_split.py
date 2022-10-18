#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

SOURCE_DIR = './Migrated_TIFF'
TARGET_DIR = '../../Data/NAMSS/NAMSS_{}_HR'

split = {
    'b-01-75-at' : 'train',
    'b-01-80-at' : 'train',
    'b-01-81-at' : 'train',
    'b-01-82-at' : 'train',
    'b-01-83-at' : 'train',
    'b-01-84-at' : 'train',
    'b-01-88-at' : 'train',
    'b-02-77-at' : 'train',
    'b-02-79-at' : 'train',
    'b-02-80-at' : 'train',
    'b-02-81-ar' : 'train',
    'b-02-82-at' : 'train',
    'b-02-84-at' : 'train',
    'b-03-75-at' : 'train',
    'b-03-80-ar' : 'train',
    'b-03-81-at' : 'train',
    'b-03-82-at' : 'train',
    'b-04-80-at' : 'train',
    'b-04-81-at' : 'train',
    'b-04-82-at' : 'train',
    'b-04-83-at' : 'train',
    'b-05-81-at' : 'train',
    'b-05-83-at' : 'train',
    'b-06-76-at' : 'train',
    'b-06-79-at' : 'train',
    'b-06-82-at' : 'train',
    'b-07-76-at' : 'train',
    'b-07-78-ak' : 'train',
    'b-07-81-at' : 'train',
    'b-07-83-at' : 'train',
    'b-08-75-at' : 'train',
    'b-08-78-at' : 'train',
    'b-08-83-at' : 'train',
    'b-09-75-at' : 'train',
    'b-09-81-at' : 'train',
    'b-10-80-at' : 'train',
    'b-10-81-at' : 'train',
    'b-10-82-at' : 'train',
    'b-11-77-at' : 'train',
    'b-11-78-at' : 'train',
    'b-11-82-at' : 'train',
    'b-11-88-at' : 'train',
    'b-12-77-at' : 'train',
    'b-13-76-at' : 'train',
    'b-13-78-at' : 'train',
    'b-15-77-ak' : 'train',
    'b-15-79-at' : 'train',
    'b-15-87-ar' : 'train',
    'b-16-76-at' : 'train',
    'b-16-77-at' : 'train',
    'b-17-77-at' : 'train',
    'b-23-81-ar' : 'train',
    'b-25-77-ak' : 'train',
    'b-28-75-at' : 'train',
    'b-29-76-at' : 'train',
    'b-30-82-ar' : 'train',
    'b-32-84-ar' : 'train',
    'b-33-77-ak' : 'train',
    'b-59-82-ar' : 'train',
    'b-60-82-ar' : 'train',
    'h-14-79-sc' : 'train',
    'h-17-79-sc' : 'train',
    'h-18-79-sc' : 'train',
    'j-1-88-sc' : 'train',
    'l-09-11-ga-mcs' : 'train',
    'l-11-11-bs-mcs' : 'test',
    'l-12-82-wg' : 'train',
    'w-1-70-sc' : 'train',
    'w-1-79-cb' : 'valid',
    'w-10-78-sc' : 'train',
    'w-10-79-bs' : 'test',
    'w-12-79-eg' : 'train',
    'w-13-77-sc' : 'train',
    'w-13-79-ar' : 'train',
    'w-14-76-sf' : 'valid',
    'w-14-79-wg' : 'train',
    'w-16-76-sf' : 'valid',
    'w-16-77-bs' : 'test',
    'w-17-79-nc' : 'valid',
    'w-18-75-np' : 'test',
    'w-2-70-sc' : 'train',
    'w-2-75-wg' : 'train',
    'w-20-79-ar' : 'train',
    'w-21-80-bs' : 'test',
    'w-22-79-np' : 'valid',
    'w-23-81-sc' : 'train',
    'w-25-80-ar' : 'train',
    'w-26-80-wg' : 'train',
    'w-26-80-wo' : 'test',
    'w-27-81-cs' : 'train',
    'w-29-80-wo' : 'test',
    'w-3-75-sc' : 'train',
    'w-3-79-cb' : 'valid',
    'w-30-81-cs' : 'train',
    'w-30-81-sc' : 'train',
    'w-31-81-bs' : 'test',
    'w-31-81-sc' : 'train',
    'w-32-82-cc' : 'train',
    'w-33-81-ar' : 'train',
    'w-33-82-sc' : 'train',
    'w-34-82-aa' : 'train',
    'w-34-82-mb' : 'valid',
    'w-35-82-nc' : 'valid',
    'w-36-83-sc' : 'train',
    'w-37-84-sc' : 'train',
    'w-38-83-sc' : 'train',
    'w-39-85-wo' : 'test',
    'w-4-74-sc' : 'train',
    'w-4-77-sa' : 'test',
    'w-4-82-nc' : 'valid',
    'w-40-80-ak' : 'train',
    'w-40-85-sc' : 'train',
    'w-5-75-sc' : 'train',
    'w-5-82-sc' : 'train',
    'w-50-70-cs' : 'train',
    'w-6-75-nc' : 'valid',
    'w-6-78-bs' : 'test',
    'w-6-85-sc' : 'train',
    'w-67-82-wg' : 'train',
    'w-9-78-nc' : 'valid',
    'w-9-79-ar' : 'train',
    'w-95-92-sa' : 'test'
}


print("\nThis script will move every file from", SOURCE_DIR, "to", TARGET_DIR.format("{train/valid/test}")+",", "and erase the source directory.\n")

input("Press ENTER to continue or Ctrl+C to abort.")
print()

for i, survey in enumerate(split, start=1):
    print("\rProcessing survey", i, "of", len(split), flush=True, end='')

    split_set = split[survey]

    read_dir = os.path.join(SOURCE_DIR, survey)
    save_dir = TARGET_DIR.format(split_set)
    fnames = os.listdir(read_dir)
    target_fname = survey + ".{}"
    source_files = [os.path.join(read_dir, f) for f in fnames]
    target_files = [os.path.join(save_dir, target_fname.format(f)) for f in fnames]

    os.makedirs(save_dir, exist_ok=True)

    list(map(os.rename, source_files, target_files))

    os.removedirs(read_dir)
print('\n')
