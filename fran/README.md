# Fran LLM Related assets

## Utilities

### Load Conversation
Used to load one conversation into another. This is how we load engineered prompts into a conversation, sometimes called "loading a personality"
The command takes two parameters, first is the Target Channel Name, the second is a csv file with message content. See files in [personalities](./personalities/) for examples.
```sh
load_conversation.sh Echo ./personalities/echo.csv
```

### Start Conversation
Used to reset a channel before loading the conversation. Takes the same arguments as Load Conversation
```sh
start_conversation.sh Echo ./personalities/fran_base.csv
```

## Personalities
Personalities are csv files that contain messages for an engineered prompt. These files are "loaded" into a conversation with the load_conversation script. 
These files are intended to be used in a layered fashion, that can support more than just Fran, with other specialized agents to follow. To run fran you should start by loading the personalities into the system with.
```sh
./start_conversation.sh Fran_base ./personalities/fran_base.csv
./start_conversation.sh Echo ./personalities/echo.csv
./start_conversation.sh Tool ./personalities/tool.csv
./start_conversation.sh Fran ./personalities/fran.csv
./start_conversation.sh Exercise ./personalities/fran_exercise.csv
```
Each of these prompts are meant to be incremental. 
- Fran_base establishes the name Fran
- Echo Teaches Fran how to participate in a group conversation
- Tool Teaches Fran how to access agent/action tools 
- Fran Teaches Fran how to be a design thinking workshop facilitator
- Exercise Teaches Fran how to be a design thinking exercise specialist. 

Once you have created the named conversations above you can load those into a new conversation with the @mention load command, the load_conversation action, or the /conversation/load api endpoint. This might be how you started a conversation in a discord channel.
```
@fran_the_facilitator join
@fran_the_facilitator reset
@fran_the_facilitator load Fran_base
@fran_the_facilitator load Echo
```
That should be enough to cary on group conversations in a channel. 