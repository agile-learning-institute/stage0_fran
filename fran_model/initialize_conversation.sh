#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <channel_id> <csv_file>"
    exit 1
fi

CHANNEL_ID="$1"
CSV_FILE="$2"

# Verify that the file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: File '$CSV_FILE' not found!"
    exit 1
fi

# Make API request
curl -s -X POST "http://localhost:8580/api/conversation/$CHANNEL_ID/initialize" \
    -H "Content-Type: text/csv" \
    --data-binary "@$CSV_FILE" > /dev/null
