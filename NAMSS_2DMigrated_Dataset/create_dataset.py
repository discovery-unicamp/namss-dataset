import argparse
import os
import numpy as np
import pandas as pd
from imageio import imsave
from pathlib import Path
from aux import read_segy
from tqdm.contrib.concurrent import thread_map
import traceback


def segy_as_img(segy_file, img_format="tiff"):
    if img_format in ["png", "jpg"]:
        drange = [0, 255]
        dtype = np.uint8
    elif img_format == "tiff":
        drange = [-1.0, 1.0]
        dtype = np.float32
    else:
        raise RuntimeError("Cannot save data as image format " + img_format)

    data = read_segy.read_seismic_data(segy_file)
    data = read_segy.normalize(data, drange, dtype)
    return data


def process_row(args_tuple):
    # Faz um unpack
    row_idx, row, args, output_path = args_tuple
    try:
        # Input file
        survey = Path(args.input_dir) / row["SURVEY"] / row["FILE"]

        # Output directory
        split_dir = output_path / row["SPLIT"].lower()
        split_dir.mkdir(parents=True, exist_ok=True)

        # Output filename (remove .segy/.sgy if present)
        fname = row["FILE"]
        if fname.lower().endswith((".segy", ".sgy")):
            fname = fname.rsplit(".", 1)[0]

        img_file = split_dir / f"{row_idx:04}_{row['SURVEY']}.{fname}.{args.format}"

        # Convert + save
        data = segy_as_img(survey, img_format=args.format)
        imsave(img_file, data)
        return True

    except Exception as e:
        print(f"Error processing {row.get('FILE')} ({row_idx}): {e}")
        print(traceback.format_exc())
        return False

def main():
    parser = argparse.ArgumentParser(description="Create NAMSS 2D Migrated Dataset")
    parser.add_argument("--input_dir", type=str, default="./Migrated_Files")
    parser.add_argument(
        "--output_dir", type=str, default="../Data/unicamp-namss-dataset"
    )
    parser.add_argument("--surveys_list", type=str, default="curated_survey_list.csv")
    parser.add_argument(
        "--format",
        type=str,
        default="tiff",
        choices=["png", "jpg", "tiff"],
        help="Image format to save",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers to use",
    )
    args = parser.parse_args()

    surveys_list = pd.read_csv(args.surveys_list, sep="\t")
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {output_path}")
    print(f"Using {args.workers} threads")

    tasks = [(idx, row, args, output_path) for idx, row in surveys_list.iterrows()]
    print(f"There are {len(tasks)} SEG-Y files to process.")

    results = thread_map(
        process_row,
        tasks,
        max_workers=args.workers,
        desc="Processing SEG-Y files",
        chunksize=1,
        total=len(tasks),
    )
    success_count = sum(1 for r in results if r)
    print(f"Processed {success_count} out of {len(tasks)} files successfully.")


if __name__ == "__main__":
    main()
