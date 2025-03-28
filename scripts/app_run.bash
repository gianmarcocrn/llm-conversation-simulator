#!/bin/bash

# Check if the user provided model and context length as arguments
if [ $# -lt 2 ]; then
    echo "Error - Not enough arguments were given"
    echo "Usage: $0 <model> <context-length>"
    echo "Example: $0 mlx-community/Llama-3.2-3B-Instruct-4bit 50000"
    exit 1
fi

MODEL=$1
CONTEXT_LENGTH=$2

lms server start
lms load $MODEL --context-length=$CONTEXT_LENGTH --gpu=1.0

python ./src/main.py $MODEL

lms unload --all
lms server stop