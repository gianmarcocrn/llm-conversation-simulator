#!/bin/bash

# Check if the user provided model, conversation log directory name and persona setting directory name as arguments
if [ $# -lt 3 ]; then
    echo "Error - Not enough arguments were given"
    echo "Usage: $0 <model> <conversation-log-directory-name> <persona-setting-directory-name>"
    echo "Example: $0 mlx-community/Llama-3.2-3B-Instruct-4bit conversations personas"
    exit 1
fi

MODEL=$1
CONV_LOG_DIRECTORY=$2  # Name of folder containing conversation logs to evaluate
PERSONA_LOG_DIRECTORY=$3 # Name of folder containing persona setting files for conversations above

# Loop through each file in the directory
for FILE1 in "$CONV_LOG_DIRECTORY"/*; do
    echo "Evaluating: $FILE1"
    # Extract timestamp (assuming format: conversation_log_new_personas_DD-MM-YYYY_HH:MM:SS.ext)
    TIMESTAMP=$(echo "$FILE1" | grep -oE '[0-9]{2}-[0-9]{2}-[0-9]{4}_[0-9]{2}:[0-9]{2}:[0-9]{2}')
    
    if [[ -n "$TIMESTAMP" ]]; then  # Ensure a timestamp was found
        # Find the two persona files with the same timestamp
        FILES=($(find "$PERSONA_LOG_DIRECTORY" -type f -name "*$TIMESTAMP*" ! -name "$(basename "$FILE1")"))
        if [[ ${#FILES[@]} -ge 2 ]]; then
            FILE2="${FILES[0]}"
            FILE3="${FILES[1]}"
            echo "First matching persona file: $FILE2"
            echo "Second matching persona file: $FILE3"
            # Strip directory part
            FILE1_NAME=$(basename "$FILE1")
            FILE2_NAME=$(basename "$FILE2")
            FILE3_NAME=$(basename "$FILE3")

            echo "Running: ./scripts/eval_run_no_load.bash $MODEL $FILE1_NAME $FILE2_NAME"
            ./scripts/eval_run_no_load.bash $MODEL $FILE1_NAME $FILE2_NAME
            
            echo "Running: ./scripts/eval_run_no_load.bash $MODEL $FILE1_NAME $FILE3_NAME"
            ./scripts/eval_run_no_load.bash $MODEL $FILE1_NAME $FILE3_NAME
        else 
            echo "Not enough matching persona files found for: $(basename "$FILE1")"
        fi
    fi
done