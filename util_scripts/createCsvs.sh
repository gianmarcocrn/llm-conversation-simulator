#!/bin/bash

# Find all .xlsx files and process them
find . -type f -name "*.xlsx" | while read xlsx_file; do
    dir=$(dirname "$xlsx_file")  # Get directory of the xlsx file

    # Find the corresponding .txt file in the same directory
    txt_file=$(find "$dir" -maxdepth 1 -type f -name "experiment*_log_*.txt" | head -n 1)

    if [[ -f "$txt_file" ]]; then
        txt_filename=$(basename "$txt_file")  # Extract filename from path
        csv_filename="evaluation_${txt_filename%.txt}.csv"  # Construct new CSV filename

        csv_file="$dir/$csv_filename"  # Set output CSV file path
        ssconvert "$xlsx_file" "$csv_file"
        echo "Converted: $xlsx_file -> $csv_file"
    else
        echo "No matching .txt file found for: $xlsx_file"
    fi
done

echo "All conversions completed!"
