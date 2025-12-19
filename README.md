# Unicamp NAMSS 2D Migrated Dataset

This repository contains code to download, process, and analyze the Unicamp NAMSS 2D Migrated Dataset. This dataset consists of seismic data collected during the North Atlantic Margin Seismic Survey (NAMSS) project.

## Installation

In order to set up the required environment, we use conda environments. To create and activate the environment, run the following commands:

```bash
conda env create -f environment.yml
conda activate namss
```

## Quick Start

The repository includes scripts to download and process the dataset, as well as Jupyter notebooks for analysis and visualization.
There are several ways to customize the dataset processing, which user may refer to the `NAMSS_Metadata` and `NAMSS_2DMigrated_Dataset` README files for more details.
We already made available many of default values and configurations to facilitate the quick start.

### Download Original Data

To download the dataset, run the following command:

```bash
cd NAMSS_2DMigrated_Dataset
./download_migrated_data.sh 
# Survey W-29-80-WO direct file links are broken, so we download manually:
./download_w-29-80-wo.sh
```

This script will read all CSV files in `NAMSS_2DMigrated_Dataset/Migrated_Balanced` folder, download all files listed in it and save it into `NAMSS_2DMigrated_Dataset/Migrated_files` folder, which will contain a subfolder for each survey, and each survey folder will contain the downloaded SEGY files.

### SEGY to TIFF Conversion

Once the dataset is downloaded, convert the SEGY files to TIFF images by running:

```bash
cd NAMSS_2DMigrated_Dataset
python segy_to_img.py
```

This will save TIFF images in the `NAMSS_2DMigrated_Dataset/Migrated_TIFF` folder.

### Creating Dataset Splits

To create training, validation, and test splits of the dataset, run:

```bash
cd NAMSS_2DMigrated_Dataset
python create_dataset_from_tiff.py
```

This script will split the dataset and save the splits in the `Data/NAMSS/NAMSS_{train/val/test}` folders.

## Analysis Scripts

The `Analysis` folder contains scripts for visualizing the embeddings extracted from the dataset. These scripts utilize libraries such as Plotly, UMAP, and Pytorch to extract, reduce dimensions, and visualize the embeddings. The pipeline includes:
1. **Embedding Extraction**: Extract embeddings from the dataset using pre-trained models, including: ResNet50 (pretrained with COCO) and DINOv2 (pretrained with LVD-142M). For each image, a fixed-size embedding is extracted and saved for further analysis.
2. **Dimensionality Reduction**: Apply UMAP to reduce the dimensionality of the extracted embeddings to 2D space for visualization.
3. **Visualization**: Generate scatter plots of the 2D embeddings, colored by various metadata attributes such as year, survey, and acquisition parameters.

> **NOTE**: Step 1 can be a computationally intensive process. Please ensure you have access to a machine with a compatible GPU and sufficient memory to handle the dataset.

### Embedding-Space Variability Figures

The `Analysis/plots_namss.py` script is used to generate the embedding-space variability figures (Figure 5 in the paper). It will create UMAP visualizations of the embeddings extracted from the NAMSS dataset. You may change `METADATA_ALL_PATH`, `DATA_PATH`, and `UMAP_FIGURES_PATH` variables to point to your dataset and desired output locations, if needed. Then, run the script using:

```bash
cd Analysis
python plots_namss.py
```

This will generate and save the UMAP plots in the specified output directory, colored by different metadata attributes (year, macro-region, and survey).

### Relationship of Unicamp-NAMSS to other seismic datasets

We also provide scripts that compares the Unicamp-NAMSS dataset to other seismic datasets, such as the Netherlands F3 dataset and the AI-Crowd's SEAM-AI dataset (Figure 6 in the paper). In order to run these scripts, you first need to download and extract the Netherlands F3 dataset and the SEAM-AI dataset. They can be found at:
- Netherlands F3 dataset: https://zenodo.org/record/3755060/files/raw.zip (does not need registration). Extract and use the `seismic_entire_volume.npy` file.
- SEAM-AI dataset: https://www.aicrowd.com/challenges/seismic-facies-identification-challenge (needs registration). Download the data_train.npy file.
    
Once downloaded and extracted, you may update the paths in the `Analysis/plots_compare_datasets.py` script to point to the respective dataset files. Then, run the script using:

```bash
cd Analysis
python plots_compare_datasets.py
```

This will generate UMAP visualizations comparing the embeddings from the Unicamp-NAMSS dataset with those from the Netherlands F3 and SEAM-AI datasets, and save the plots in the specified output directory.
