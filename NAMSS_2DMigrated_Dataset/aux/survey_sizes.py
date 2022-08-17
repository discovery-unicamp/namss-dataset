#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

#readdir = '../Migrated_Balanced'
readdir = '../Migrated_CSV'


def read_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        csvrows = [row for row in reader]
    return csvrows


def main():
    files = os.listdir(readdir)
    files.sort()

    all_datasets_size = 0.0
    vmin = 10**12
    vmax = 0
    for fname in files:
        csvrows = read_csv(os.path.join(readdir, fname))
        total_size = 0
        for _, size in csvrows:
            size = float(size)
            total_size += size
        print(os.path.splitext(fname)[0], "{:.1f}".format(total_size), len(csvrows), sep='\t')

        if vmin > total_size:
            vmin = total_size
            vmin_data = fname
        if vmax < total_size:
            vmax = total_size
            vmax_data = fname
        all_datasets_size += total_size

    print()
    print("MIN: {} {:.2f}".format(vmin_data, vmin))
    print("MAX: {} {:.2f}".format(vmax_data, vmax))
    print("TOTAL: {:.2f}".format(all_datasets_size))



if __name__ == '__main__':
    main()
