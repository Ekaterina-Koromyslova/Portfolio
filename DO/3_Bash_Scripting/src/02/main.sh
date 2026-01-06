#!/bin/bash

source "./lib/help_functions.sh"
source "./lib/assemble_data.sh"
source "./lib/create_output.sh"

echo
read -p "Do you want to save this data to a file? (Y/N): " answer

if [[ "$answer" == "Y" || "$answer" == "y" ]]; then
    filename="$(date +"%d_%m_%y_%H_%M_%S").status"
    source ./lib/assemble_data.sh > "$filename"
    source ./lib/create_output.sh >> "$filename"
    echo "Saved to $filename"
else
    echo "Not saved."
fi
