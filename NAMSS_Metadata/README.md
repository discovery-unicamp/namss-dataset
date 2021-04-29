## Gathering NAMSS Metadata

The National Archive of Marine Seismic Surveys (NAMSS) provides free and open access to hundreds of seismic surveys (DOI:10.5066/F7930R7P).
These scripts help to collect metadata for a set of surveys by parsing associated XML and HTML web pages.
As is the case with any parser, these scripts probably do not have a long shelf-life and are expected to break, as the NAMSS website evolves and it's HTML structure changes.

To collect metadata in bulk, perform the following steps:

1. Filter surveys from the search tool available at https://walrus.wr.usgs.gov/namss/search/ and download one or more CSV lists. Save them in the `Collected_CSVs` directory. 
2. Use the `combine_CSVs.py` script to merge and save all collected CSVs and remove duplicate surveys.
3. Download the available information for the selected set of surveys with `download_metadata.py`. Metadata for each survey is saved as a separate JSON file.
4. To merge all the information in a single table, use the `json_to_CSV.py` script, which generates a tab-separated CSV file, with column headers.

The saved CSV and JSON files in this repository is a gathering of metadata regarding all 2D Multichannel Seismic surveys available in April, 2021.



