# Fran LLM Related assets

## Utilities
We use pipenv to anchor automation related to creating and testing the prompts used by the Fran chat bot. 

### Load Prompts
```sh
pipenv run initialize
```
This uses the [start_everything.sh](./start_everything.sh) script to load the prompts/.csv files, and create the FRAN conversation from selected prompts. 

### Run prompt evaluation pipeline
```sh
pipenv run evaluate
```
This will run the Echo Evaluation pipeline using the folders in ``fran_model``

### Run Grader evaluation pipeline
```sh
pipenv run grade
```
This will run the Echo Grader pipeline using the folders in ``fran_model``

## [Conversations](./conversations/)
Conversations used for evaluation purposes. The conversation is processed message by message.
The model generates a reply for steps were the actor is assistant, that is then graded against the value provided in the test conversation. 

## [Grader](./grader/)
These are the prompts used by the evaluation process when grading a response against the desired value. We are using AI to grade AI.

## [Prompts](./prompts/)
Prompts are csv files that contain messages for an engineered prompt. These files are "loaded" into a conversation with the load_conversation script. 
These files are intended to be used in a layered fashion, that can support more than just Fran, with other specialized agents to follow. The prompts are:
- echo.csv: The basic echo bot prompt
- tools.csv: Adds the Agent/Action tools functionality 
- fran.csv: Basic Fran prompt
- design.csv: Fran and Stage0 Design Thinking
- exercise.csv: Fran exercise prompt basics

The start_everything script currently loads all of those csv files to conversations of the same name, and then loads ``design``, ``echo``, ``tools``, ``fran`` to a FRAN conversation you can use with ``@fran_the_facilitator load FRAN`` to load the full prompt in a conversation.