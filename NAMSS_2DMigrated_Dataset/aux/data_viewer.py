#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
import numpy as np

from read_segy import read_seismic_data, normalize


# Parse input arguments 
def get_arguments():
    parser = argparse.ArgumentParser()

    # Mandatory argument
    parser.add_argument("segy_file", help=("Seismic SEGY file to be opened."))

    # Optional arguments
    parser.add_argument("--normalize", action='store_true',
                        help=("Normalize the dynamic range to [-1.0, 1.0]."))

    parser.add_argument("--clip", default=1.0, type=float, metavar="(0.0, 1.0]",
                        help=("Clip factor in image viewing. "
                        "Default: 0.5."))

    parser.add_argument("--vmax", default=None, type=float, 
                        help=("Max value for plotting. If unset, gets max from data."))

    parser.add_argument("--color", default='seismic',
                        help=("Color scheme to plot the seismic data. "
                        "Default: seismic."))

    parser.add_argument("--print-header", action='store_true',
                        help=("Prints textual header. "))

    args = parser.parse_args() 
    if not 0.0 < args.clip <= 1.0:
        import sys
        sys.exit("Error: clip factor must in the range (0.0, 1.0].")

    return args


def print_textual_header(segy_file):
    with open(segy_file, 'rb') as f:
        textual_header = f.read(3200)
        encoding = 'cp500'
        if textual_header.isascii():
            encoding = 'utf-8'
        textual_header = textual_header.decode(encoding)
        textual_header = [textual_header[i:i+80] for i in range(0, len(textual_header), 80)]
        textual_header = "\n".join(textual_header) 
        
    print(textual_header)
    print()


def view_data(img, color='seismic', vmax=None, clip=1.0):
    if vmax is None:
        vmax = np.abs(img).max()

    vmax *= clip

    print("Dimensions:", img.shape)
    print("Dynamic range:", img.min(), img.max())
    print("Type:", img.dtype)

    plt.imshow(img, vmin=-vmax, vmax=vmax, cmap=color, interpolation='nearest')
    plt.colorbar()
    plt.show()


def main():
    args = get_arguments()

    if args.print_header:
        print_textual_header(args.segy_file)

    data = read_seismic_data(args.segy_file)
    if args.normalize:
        data = normalize(data, [0,1])

    view_data(data, args.color, args.vmax, args.clip)


if __name__ == '__main__':
    main()
