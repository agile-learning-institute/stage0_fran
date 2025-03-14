#!/bin/bash

./fran_model/initialize_conversation.sh echo ./fran_model/prompts/echo.csv
./fran_model/initialize_conversation.sh exercise ./fran_model/prompts/exercise.csv
./fran_model/initialize_conversation.sh fran_base ./fran_model/prompts/fran_base.csv
./fran_model/initialize_conversation.sh fran ./fran_model/prompts/fran.csv
./fran_model/initialize_conversation.sh tools ./fran_model/prompts/tools.csv
