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

# Read the CSV file line by line
while IFS=, read -r role from to text; do
    # Trim leading/trailing whitespace
    role=$(echo "$role" | xargs)
    from=$(echo "$from" | xargs)
    to=$(echo "$to" | xargs)

    # Extract text (handling embedded commas correctly)
    text=$(echo "$text" | sed 's/^ *//g')

    # Construct JSON payload
    JSON_DATA=$(jq -n \
                  --arg role "$role" \
                  --arg from "$from" \
                  --arg to "$to" \
                  --arg text "$text" \
                  '{role: $role, content: ("From:" + $from + ", To:" + $to + " " + $text)}')

    # Make API request
    curl -s -X POST "http://localhost:8580/api/conversation/$CHANNEL_ID/message" \
         -H "Content-Type: application/json" \
         -d "$JSON_DATA" > /dev/null

    echo "$role sent message as $from to $to message $text"

done < <(tail -n +2 "$CSV_FILE")  # Skip header row