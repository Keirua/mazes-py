#!/bin/bash

# Array of file names
file_names=("003.png" "006.png" "009.png" "025.png" "151.png" "813.png" "831.png")

# Loop over the file names
for filename in "${file_names[@]}"
do
    # Run the command with the current filename
    poetry run python mask_from_img.py "$filename"
done
