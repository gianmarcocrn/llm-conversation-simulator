import csv
import json
import argparse
import os

# Change as required
OUTPUT_DIR_NAME = "eval_results_json"

def create_eval_dict(row):
    """Convert a CSV row into the desired evaluation dictionary format."""
    return {
        "consistency": {"rating": row.get("Consistency", "")},
        "relevance": {"rating": row.get("Relevance", "")},
        "naturalness": {"rating": row.get("Naturalness", "")},
        "fluency": {"rating": row.get("Fluency", "")}
    }

def main(csv_file_path):
    # Create an output directory for evaluations
    output_dir = OUTPUT_DIR_NAME
    os.makedirs(output_dir, exist_ok=True)
    csv_file_name = os.path.basename(csv_file_path)
    csv_file_name_no_extension = os.path.splitext(csv_file_name)[0]

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            eval_dict = create_eval_dict(row)
            output_file_path = os.path.join(output_dir, f'persona_{idx}_{csv_file_name_no_extension}.txt')
            
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                json.dump(eval_dict, outfile, ensure_ascii=False)
            
            print(f"Saved: {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV evaluations to JSON files.")
    parser.add_argument("csv_file_path", help="Path to the CSV file")
    args = parser.parse_args()

    main(args.csv_file_path)
    print("All evaluations have been saved.")