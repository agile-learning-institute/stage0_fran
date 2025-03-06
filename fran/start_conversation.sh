#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <channel_id> <csv_file>"
    exit 1
fi

CHANNEL_ID="$1"
CSV_FILE="$2"

# Reset the conversation
curl -s -X POST "http://localhost:8580/api/conversation/$CHANNEL_ID/reset" \
     -H "Content-Type: application/json" > /dev/null
echo "Reset Conversation $CHANNEL_ID"

# Load the conversation
./load_conversation.sh $CHANNEL_ID $CSV_FILE
