#!/bin/bash
# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

folder_name=$1  # The first argument is stored in the variable 'name'

ros2 run logger syncronize_data.py /media/ubuntu/WinToUSB/datasets/$folder_name --sampling_freq 20 --resize_to "(224, 224)" --compress
