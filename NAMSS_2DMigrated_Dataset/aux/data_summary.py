#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import numpy as np
import os

from ibm2ieee import ibm2float32 
from tqdm import tqdm


SURVEYS_DIR = '../Migrated_Files'
CSV_FILE = 'data_summary_log.csv'


# SEGY file constants
TEXTUAL_HEADER_SIZE = 3200
BINARY_HEADER_SIZE = 400
TRACE_HEADER_SIZE = 240
BYTES_PER_SAMPLE = 4
IBM_SAMPLE_FORMAT = 1
IEEE_SAMPLE_FORMAT = 5

MAX_FLOAT = np.finfo(np.float32).max
ZERO = 1e-37


def read_field(stream, byte_addr):
    stream.seek(byte_addr - 1)
    return int.from_bytes(stream.read(2), 'big')


def read_trace(stream, trace_ind, trace_ns, sample_format):
    trace_size = TRACE_HEADER_SIZE + trace_ns*BYTES_PER_SAMPLE
    data_offset = TEXTUAL_HEADER_SIZE + BINARY_HEADER_SIZE + trace_ind*trace_size + TRACE_HEADER_SIZE
    stream.seek(data_offset)

    data = stream.read(trace_ns*BYTES_PER_SAMPLE)
    if not data:
        return None
    if sample_format == IBM_SAMPLE_FORMAT:
        data = np.frombuffer(data, dtype='>u4')
        data = ibm2float32(data)
    elif sample_format == IEEE_SAMPLE_FORMAT:
        data = np.frombuffer(data, dtype='>f4')
    else:
        data = None
        print("Sample format", sample_format, "not implemented.")

    return data


def read_file_info(segy_file):
    with open(segy_file, 'rb') as stream:
        info = dict()

        # Data format (3225-3226)
        sample_format = read_field(stream, 3225) 
        info['DATA FORMAT'] = sample_format

        # SEGY Revision (3501-3502)
        info['SEGY REVISION'] = read_field(stream, 3501)

        # Extended Headers (3505-3506)
        info['EXTENDED HEADERS'] = read_field(stream, 3505)

        # Num. samples per trace (3221-3222)
        trace_ns = read_field(stream, 3221)
        info['SAMPLES PER TRACE'] = trace_ns

        # Compute number of traces and total samples
        trace_size = TRACE_HEADER_SIZE + trace_ns*BYTES_PER_SAMPLE
        data_size = stream.seek(0, 2)
        num_traces = (data_size - TEXTUAL_HEADER_SIZE - BINARY_HEADER_SIZE)//trace_size
        num_samples = trace_ns * num_traces

        info['NUM TRACES'] = num_traces
        info['NUM SAMPLES'] = num_samples

        # Read data
        traces = []
        for i in range(num_traces):
            trace_data = read_trace(stream, i, trace_ns, sample_format)
            if trace_data is None:
                break
            traces.append(trace_data)
        data = np.array(traces).T

        # Get number of zeros and ratio to total num. of samples
        data_abs = np.abs(data)
        num_zeros = data_abs[data_abs <= ZERO].size

        info['NUM ZEROS'] = num_zeros
        info['N_ZERO/N_SAMP'] = num_zeros/num_samples

        # Discard zero values and replace Inf with Max Float
        data_abs = data_abs[data_abs > ZERO]
        data_abs[data_abs == np.Inf] = MAX_FLOAT

        # Get min and max from absolute non-zero values
        info['MIN ABS N0 VALUE'] = data_abs.min()
        info['MAX ABS VALUE'] = data_abs.max()

        # Get the median and average of the log of non-zero absolute samples
        logs = np.log10(data_abs)

        info['NON-0 MEDIAN LOG'] = np.median(logs)
        info['NON-0 AVG LOG'] = logs.mean()

        # Get max log and ratio of max to avg log 
        info['ABS MAX LOG'] = logs.max()
        info['MAX_LOG - AVG_LOG'] = logs.max() - logs.mean() 

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
