#!/bin/bash

# Converts csvs with evaluation results to json formatted text files using csvToJson.py
# Assumes script is run from within a results directory that it is in the same directory as util_scripts

# Check if the user provided a search string
if [ -z "$1" ]; then
  echo "Usage: $0 <search_string>"
  exit 1
fi

SEARCH_STRING="$1"
PYTHON_SCRIPT="../util_scripts/csvToJson.py"

# Find all matching CSV files that contain the search string in their filename
find . -type f -name "*.csv" | grep "$SEARCH_STRING" | while read file; do
    echo "Processing: $file"
    python "$PYTHON_SCRIPT" "$file"
done

echo "All evaluations processed!"