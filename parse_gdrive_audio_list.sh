#!/bin/sh

# Get the list of audio files from gdrive
# Here we have the actual binary in the same folder
# Otherwise we can call from path
# Use AWK to obtain only the first two columns ('Id' and 'Name')
# Save to the file 'audio_list.csv'
./gdrive-linux-x64 list -m 5000 --name-width 0 --order "name" | awk -F "[[:space:]][[:space:]][[:space:]]+" '{print $1 "," $2}' > audio_list.csv

# Parse 'audio_list.csv' into a richer CSV file that Jekyll can then use
python3 parse_gdrive_audio_csv.py

# Copy these files to 'flushinggospelhall/_data'
cp fgh_audio_list.csv ../flushinggospelhall.org/_data/