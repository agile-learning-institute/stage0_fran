#!/bin/bash

# Initialize all the layers
./fran_model/initialize_conversation.sh design ./fran_model/prompts/design.csv
./fran_model/initialize_conversation.sh echo ./fran_model/prompts/echo.csv
./fran_model/initialize_conversation.sh exercise ./fran_model/prompts/exercise.csv
./fran_model/initialize_conversation.sh fran ./fran_model/prompts/fran.csv
./fran_model/initialize_conversation.sh tools ./fran_model/prompts/tools.csv

# Build a combined prompt
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/design" -H "Content-Type: application/json" > /dev/null
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/echo" -H "Content-Type: application/json"  > /dev/null
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/tools" -H "Content-Type: application/json"  > /dev/null
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/fran" -H "Content-Type: application/json"  > /dev/null
