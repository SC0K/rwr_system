#!/bin/bash
# Check if two arguments were provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <file_name> <destination_folder>"
    exit 1
fi

file_name=$1        # The first argument is stored in 'folder_name'
destination_folder=$2   # The second argument is stored in 'destination_path'

rsync -avz -e ssh ubuntu@18.192.52.202:/home/ubuntu/srl_il/runs/$file_name /Volumes/RWR_Team4/policy/$destination_folder/
