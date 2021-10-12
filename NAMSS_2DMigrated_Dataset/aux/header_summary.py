#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

from tqdm import tqdm
from read_segy import read_field


SURVEYS_DIR = '../Migrated_Files'
#SURVEYS_DIR = '../Test_Files'
CSV_FILE = 'header_summary.csv'


# SEGY file constants
TEXTUAL_HEADER_SIZE = 3200
BINARY_HEADER_SIZE = 400
TRACE_HEADER_SIZE = 240
BYTES_PER_SAMPLE = 4
IBM_SAMPLE_FORMAT = 1
IEEE_SAMPLE_FORMAT = 5

# Trace Header bytes
TRACE_CDP = 21
TRACE_ID = 29
TRACE_SCALCO = 71
TRACE_UNITCO = 89
TRACE_NS = 115
TRACE_DT = 117


def read_file_info(segy_file):
    def ordered_cdp(l):
        o = [x2 > x1 for x1, x2 in zip(l[:-1], l[1:])]
        return min(o)

    with open(segy_file, 'rb') as stream:
        info = dict()

        # Data format (3225-3226)
        sample_format = read_field(stream, 3225) 
        info['DATA FORMAT'] = sample_format

        # Trace Sorting Code (3229-3230)
        info['SORTING CODE'] = read_field(stream, 3229)

        # Measurement System. 1 = Meters, 2 = Feet (3255-3256)
        info['MEASUREMENT SYSTEM'] = read_field(stream, 3255)

        # SEGY Revision (3501-3502)
        info['SEGY REVISION'] = read_field(stream, 3501)

        # Fixed length trace flag (3503-3504)
        info['FIXED LENGTH TRACE'] = read_field(stream, 3503)

        # Extended Headers (3505-3506)
        info['EXTENDED HEADERS'] = read_field(stream, 3505)

        # Sample interval (3217-3218)
        bin_dt = read_field(stream, 3217)
        info['BH SAMPLE INTERVAL'] = bin_dt

        # Num. samples per trace (3221-3222)
        bin_ns = read_field(stream, 3221)
        info['BINARY TRACE NS'] = bin_ns

        # Compute number of traces and total samples
        trace_size = TRACE_HEADER_SIZE + bin_ns*BYTES_PER_SAMPLE
        data_size = stream.seek(0, 2)
        num_traces = (data_size - TEXTUAL_HEADER_SIZE - BINARY_HEADER_SIZE)//trace_size

        info['EXPECTED NUM TRACES'] = num_traces

        # Read trace header info
        trace_IDs = set()
        trace_NSs = set()
        trace_DTs = set()
        trace_SCALCOs = set()
        trace_UNITCOs = set()

        trace_CDPs = list()
        DT_diff = list()
        num_traces = 0

        header_offset = TEXTUAL_HEADER_SIZE + BINARY_HEADER_SIZE
        while True:
            trace_id = read_field(stream, header_offset + TRACE_ID)
            trace_ns = read_field(stream, header_offset + TRACE_NS)
            trace_dt = read_field(stream, header_offset + TRACE_DT)
            trace_scalco = read_field(stream, header_offset + TRACE_SCALCO)
            trace_unitco = read_field(stream, header_offset + TRACE_UNITCO)
            trace_cdp = read_field(stream, header_offset + TRACE_CDP, field_size=4)

            if trace_id is None or trace_ns is None or trace_dt is None:
                break

            trace_IDs.add(trace_id)
            trace_NSs.add(trace_ns)
            trace_DTs.add(trace_dt)
            trace_SCALCOs.add(trace_scalco)
            trace_UNITCOs.add(trace_unitco)

            trace_CDPs.append(trace_cdp)

            if trace_dt != bin_dt:
                DT_diff.append(num_traces + 1)

            num_traces += 1

            # All traces are assumed to have a fixed size (number of samples on the binary header)
            header_offset += TRACE_HEADER_SIZE + bin_ns*BYTES_PER_SAMPLE

        info['TRACE IDENTIFICATION'] = ', '.join([str(tid) for tid in trace_IDs])
        info['TRACE NS'] = ', '.join([str(tns) for tns in trace_NSs])
        info['TRACE DT'] = ', '.join([str(tdt) for tdt in trace_DTs])
        info['TRACE SCALCO'] = ', '.join([str(tsc) for tsc in trace_SCALCOs])
        info['TRACE UNITCO'] = ', '.join([str(tuc) for tuc in trace_UNITCOs])

        info['DT DIFF TRACE IND'] = ', '.join([str(tdt) for tdt in DT_diff])
        info['ORDERED BY CDP'] = ordered_cdp(trace_CDPs)
        info['MIN CDP'] = min(trace_CDPs)
        info['MAX CDP'] = max(trace_CDPs)

        info['COUNTED NUM TRACES'] = num_traces

    return info


def write_csv(csvfile, dict_list):
    with open(csvfile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dict_list[0].keys(), delimiter='\t')
        writer.writeheader()
        for d in dict_list:
            writer.writerow(d)


def main():
    surveys = os.listdir(SURVEYS_DIR)
    surveys.sort()

    bar = tqdm(surveys, leave=True)
    all_info = list()
    for survey in bar:
        bar.set_description("Survey {}".format(survey), refresh=True)
        dir_path = os.path.join(SURVEYS_DIR, survey)
        segy_files = os.listdir(dir_path)
        segy_files.sort()

        for segy_file in segy_files:
            segy_path = os.path.join(dir_path, segy_file)

            file_info = dict()
            file_info['SURVEY'] = survey
            file_info['FILE'] = segy_file
            file_info.update(read_file_info(segy_path))

            all_info.append(file_info)

    write_csv(CSV_FILE, all_info)



if __name__ == '__main__':
    main()
