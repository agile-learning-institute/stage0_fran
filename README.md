# stage0_fran

This repository contains the API that supports the user interface for creating, conducting, and recording Design Thinking workshops for stage0. This API is also served as a chat agent through a discord chat-bot framework. 

See [The OpenAPI](./docs/index.html) for information on the API and Data Structures Used. 

Agents are registered for each API endpoint path (config, chain, exercise, workshop), with the action name specified for each endpoint in the operationId property. 

# Echo

Echo is a chat-bot agent framework, inspired in syntax by Flask, that maps simple chat messages following the Agent/Action syntax onto your code in the same way Flask maps HTTP events onto your code. This framework is used to support a Discord App which acts as an agent proxy. Any messages that the Discord App has access to are monitored for messages that match an Echo Command in the form of
Agent/Action
```yaml
yaml: request_body
```
When a message is seen, the action is executed, and the response is written back to the Chat where it originated. 

## Separation of Concerns

### Code designed to be extracted to a utils class.
/src
| /config - Implements, global configuration values
| /flask_utils - Flask helpers
| /llm_utils - LLM Wrapper
| /mongo_utils - Simple Mongo IO Wrapper

### Code designed to be extracted to a Echo class.
/src
| /echo/Echo.py - Echo flask-like chat agent framework

### Code specific to the API
/src
| /server.py - Initialize the server, connect to backing services
| /agents - ChatBot Agent handlers
| /routes - Http Event handlers
| /services - Business logic, supports agents/routes, uses *_utils

# Supported pipenv commands
- ``pipenv run local`` run the server locally in dev mode
- ``pipenv run start`` restart the backing database and run locally *TODO
- ``pipenv run test`` run unittest testing
- ``pipenv run stepci`` run stepci testing
- ``pipenv run build`` build container locally 
- ``pipenv run container`` build and run container

# Testing with ``curl``

## Observability endpoints

#### Config 
```sh
curl http://localhost:8580/api/config
```
#### Health 
```sh
curl http://localhost:8580/api/health
```

## Testing /api/bot endpoints 

#### Get a List all Active of Bots
```sh
curl http://localhost:8580/api/bot  
```
#### Get a single Bot
```sh
curl http://localhost:8580/api/bot/bbb000000000000000000001
```
#### Update a single Bot
```sh
curl -X PATCH http://localhost:8580/api/bot/bbb000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"description":"A New Description"}'
```
#### Get a list of active channels the bot is participating in
```sh
curl http://localhost:8580/api/bot/bbb000000000000000000001/get_channels 
```
#### Add a channel to the actives channel list
```sh
curl -X POST http://localhost:8580/api/bot/bbb000000000000000000001/channel/DISCORD_CHANNEL_NAME
```
#### Remove a channel from the active channels list
```sh
curl -X DELETE http://localhost:8580/api/bot/bbb000000000000000000001/channel/DISCORD_CHANNEL_NAME
```

## Testing /api/chain endpoints with curl

#### Get a list of all Exercise Chains
```sh
curl http://localhost:8580/api/chain
```
#### Get a single Exercise Chain
```sh
curl http://localhost:8580/api/chain/a00000000000000000000001
```

## Conversation Endpoints

#### Get a list of conversations by channel name regex
```sh
curl http://localhost:8580/api/conversation
```
#### Get a single Conversation Chain
```sh
curl http://localhost:8580/api/conversation/c00000000000000000000001
```
#### Add a message to a conversation
```sh
curl -X POST http://localhost:8580/api/conversation/DISCORD_CHANNEL_ID/message \
     -H "Content-Type: text/plain" \
     -d "This is a new message"
```

## Testing /api/exercise endpoints with curl

#### Get a list of all active exercises
```sh
curl http://localhost:8580/api/exercise
```
#### Get a single exercise
```sh
curl http://localhost:8580/api/exercise/b00000000000000000000001
```

## Testing Workshop endpoints with curl

#### Get a list of all active workshops by workshop name regex
```sh
curl "http://localhost:8580/api/workshop"
```
#### Get a list of workshops by workshop name regex
```sh
curl "http://localhost:8580/api/workshop?query=^p"
```
#### Get a specific workshop
```sh
curl "http://localhost:8580/api/workshop/000000000000000000000001"
```
#### Add a new Workshop
```sh
curl -X POST http://localhost:8580/api/workshop/new/a00000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"name":"Super Duper Workshop"}'
```
#### Update a workshop
```sh
curl -X PATCH http://localhost:8580/api/workshop/000000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"name":"Updated Workshop Name"}'
```
#### Start a workshop - Status to active
```sh
curl -X PATCH http://localhost:8580/api/workshop/000000000000000000000001/start
```
#### Advance to the next exercise in the workshop
```sh
curl -X POST http://localhost:8580/api/workshop/000000000000000000000001/next
```
#### Add an observation to the current exercise
```sh
curl -X POST http://localhost:8580/api/workshop/000000000000000000000001/observation \
     -H "Content-Type: application/json" \
     -d '{"name":"Observation1"}'
```
