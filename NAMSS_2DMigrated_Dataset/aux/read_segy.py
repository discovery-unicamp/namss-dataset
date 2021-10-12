# This reader assumes same length traces and will throw an error otherwise
# Only 4-byte IBM and IEEE floating-point data sample formats are implemented.

import numpy as np
import warnings

from ibm2ieee import ibm2float64 


# SEGY file constants
TEXTUAL_HEADER_SIZE = 3200
BINARY_HEADER_SIZE = 400
TRACE_HEADER_SIZE = 240
BYTES_PER_SAMPLE = 4

# SEGY Codes
IBM_SAMPLE_FORMAT = 1
IEEE_SAMPLE_FORMAT = 5
DEAD_TRACE_ID = 2
SEISMIC_TRACE_ID = 1


def read_field(stream, byte_addr, field_size=2):
    stream.seek(byte_addr - 1)
    field = stream.read(field_size)
    if not field:
        return None
    else:
        return int.from_bytes(field, 'big', signed=True)


def read_trace_data(stream, trace_ind, bin_ns, sample_format, mute_dead_trace=True):
    trace_size = TRACE_HEADER_SIZE + bin_ns*BYTES_PER_SAMPLE
    trace_header_offset = TEXTUAL_HEADER_SIZE + BINARY_HEADER_SIZE + trace_ind*trace_size

    # Trace num. samples (Trace Header 115-116)
    trace_ns = read_field(stream, trace_header_offset + 115)

    # Trace Identification Code (Trace Header 29-30)
    trace_id = read_field(stream, trace_header_offset + 29)
    if trace_id == DEAD_TRACE_ID:
        if mute_dead_trace:
            print(trace_ind, "is dead")
            return np.zeros(trace_ns, dtype=np.float32)
    # Only reads seismic data
    elif trace_id != SEISMIC_TRACE_ID:
        warnings.warn("Trace {} not read because it is not seismic data (code {}).".format(trace_ind, trace_id))
        return None

    # Read and convert data to NumPy array
    data_offset = trace_header_offset + TRACE_HEADER_SIZE
    stream.seek(data_offset)
    # Reads only trace_ns samples
    data = stream.read(trace_ns*BYTES_PER_SAMPLE)
    if not data:
        return None
    if sample_format == IBM_SAMPLE_FORMAT:
        data = np.frombuffer(data, dtype='>u4')
        data = ibm2float64(data)
    elif sample_format == IEEE_SAMPLE_FORMAT:
        data = np.frombuffer(data, dtype='>f4')
    # Raise exception if sample format is not IBM or IEEE
    else:
        raise ValueError("Cannot read sample format {}".format(sample_format))

    return data


def read_seismic_data(segy_file):
    with open(segy_file, 'rb') as stream:
        # Data format (3225-3226)
        sample_format = read_field(stream, 3225) 

        # Binary Header num. samples per trace (3221-3222)
        bin_ns = read_field(stream, 3221)

        # First trace num. samples (Trace Header 115-116)
        first_trace_ns = read_field(stream, TEXTUAL_HEADER_SIZE + BINARY_HEADER_SIZE + 115)

        # Compute total number of traces, assuming fixed length traces
        trace_size = TRACE_HEADER_SIZE + bin_ns*BYTES_PER_SAMPLE
        data_size = stream.seek(0, 2)
        num_traces = (data_size - TEXTUAL_HEADER_SIZE - BINARY_HEADER_SIZE)//trace_size

        # Read data
        traces = []
        for i in range(num_traces):
            trace_data = read_trace_data(stream, i, bin_ns, sample_format, mute_dead_trace=False)
            if trace_data is None:
                continue
            if len(trace_data) != first_trace_ns:
                raise RuntimeError("Cannot read data with variable length traces.")
            traces.append(trace_data)
        data = np.array(traces).T

    return data


# Assumes data is in the range [-data_max, data_max].
# Normalize in the range [-range, range] if 'range' is a scalar
# or [range[0], range[1]] otherwise.
# Cast it to dtype if it's not None
def normalize(data, range=1.0, dtype=None):
    data = data.copy()
    data_max = np.abs(data).max()
    if data_max > 0:
        data /= data_max

    if np.isscalar(range):
        data *= range
    else:
        diff = range[1] - range[0]
        data *= (diff/2)
        data += (diff/2) + range[0]

    if dtype is not None:
        data = data.astype(dtype)

    return data
