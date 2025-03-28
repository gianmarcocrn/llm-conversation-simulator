#!/bin/bash

# Usage: ./app_run_in_batch.sh 30 mlx-community/meta-llama-3.1-8b-instruct 10000

# Check that two arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <number_of_runs> <model_signature> <model_context_size>"
    exit 1
fi

NUM_RUNS=$1
MODEL=$2
CONTEXT_LENGTH=$3

lms server start
lms load $MODEL --context-length=$CONTEXT_LENGTH --gpu=1.0

eval "for run in {1..$NUM_RUNS}; do ./scripts/app_run_no_load.bash $MODEL; done"

lms unload --all
lms server stop
