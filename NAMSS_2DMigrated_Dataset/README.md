# Downloading Migrated SEGY Files

Each survey can be downloaded as a single ZIP file. However, beyond the targeted migrated files, each one may come with a miscellany of data files: stacked SEGY files, navigation and velocity files, TIFF or JPEG images, PDF reports etc.
But, since we're only interested in downloading _some_ of the migrated files, it's more efficient in most cases to download each file individually, even though they are uncompressed.

This set of scripts perform four major tasks: for each survey, download the direct link to each available file and file size information, and filter the migrated SEGY files; balance each survey size (in MB) by randomly selecting a subset of available migrated data; split the surveys into training, validation and test datasets and download the files; for each SEGY file, extract the data samples from each trace and save the file as TIFF image, normalized in the range [-1, 1].

Follow the steps bellow to accomplish each task.


## 1. Collecting Migrated File Links

With the previous `../NAMSS_Metadata` scripts, it's possible to collect and generate a CSV file with the available metadata for all surveys. Manually inspect them, specially the `datasetInformation.processedDataClass` field, to determine which surveys may contain migrated data. Assemble a new two-column, no header, tab-separated CSV file, with the first column containing the Survey ID and the second the link to each dataset web page. View the `survey_dataset_links.csv` file as an example.

Set the appropriate variables and run the `download_survey_file_links.py` script to download the direct links. Each survey is saved as a two-column, no header CSV file, with the first being the direct link to the file and the second the file size in MB.

Run the `filter_migrated_links.py` script to select only links to SEGY files corresponding to migrated data*. A new folder is created, with a CSV file for each survey containing only links to migrated data.

\*The filtering is done by matching the link text to patterns that seems to correlate with migrated data at the time of creation of this repository.
As new surveys are added to the NAMSS platform, these patterns may change or break, so you may want to do your own analysis to establish filtering criteria.
You may use the `aux/analyse_patterns.py` to help in this task.





The saved CSV files in this repository is a gathering of the direct links to the migrated files of all 2D Multichannel Seismic surveys found in April, 2021.



