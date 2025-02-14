#!/bin/bash

# Check if the user provided model, conversation log filename and persona setting filename as arguments
if [ $# -lt 3 ]; then
    echo "Error - Not enough arguments were given"
    echo "Usage: $0 <model> <conversation-filename> <persona-file-name>"
    echo "Example: $0 mlx-community/Llama-3.2-3B-Instruct-4bit conversation.txt persona.txt"
    exit 1
fi

MODEL=$1
CONVERSATION_FILE_NAME=$2
PERSONA_FILE_NAME=$3

python ./src/eval_main.py $MODEL $CONVERSATION_FILE_NAME $PERSONA_FILE_NAME
