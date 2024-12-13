#!/bin/bash
# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

folder_name=$1  # The first argument is stored in the variable 'name'

rsync -avz -e ssh ubuntu@18.192.52.202:/home/ubuntu/srl_il/runs/$folder_name /Volumes/RWR_Team4/policy/

