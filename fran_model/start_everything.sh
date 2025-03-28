#!/bin/bash

# Initialize all the layers
./fran_model/initialize_conversation.sh echo ./fran_model/prompts/echo.csv
./fran_model/initialize_conversation.sh tools ./fran_model/prompts/tools.csv
./fran_model/initialize_conversation.sh design ./fran_model/prompts/design.csv
./fran_model/initialize_conversation.sh workshop ./fran_model/prompts/workshop.csv
./fran_model/initialize_conversation.sh exercise ./fran_model/prompts/exercise.csv

# Build FRAN combined prompt
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/echo" -H "Content-Type: application/json" > /dev/null
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/tools" -H "Content-Type: application/json"  > /dev/null
curl -s -X POST "http://localhost:8580/api/conversation/FRAN/load/design" -H "Content-Type: application/json"  > /dev/null
