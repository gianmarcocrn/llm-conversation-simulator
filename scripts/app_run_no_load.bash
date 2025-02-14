#!/bin/bash

# Check if the user provided model as argument
if [ $# -lt 1 ]; then
    echo "Error - Not enough arguments were given"
    echo "Usage: $0 <model>"
    echo "Example: $0 mlx-community/Llama-3.2-3B-Instruct-4bit"
    exit 1
fi

MODEL=$1

python ./src/main.py $MODEL
