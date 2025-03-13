#!/bin/bash

./start_conversation.sh echo ./prompts/echo.csv
./start_conversation.sh exercise ./prompts/exercise.csv
./start_conversation.sh fran_base ./prompts/fran_base.csv
./start_conversation.sh fran ./prompts/fran.csv
./start_conversation.sh tools ./prompts/tools.csv
