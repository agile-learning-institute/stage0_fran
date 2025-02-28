# stage0_fran

This repository contains the API and Discord Chatbot that supports the user interface for creating, conducting, and recording Design Thinking workshops for stage0. This API is also served as a chat agent through a discord chat-bot framework. 

See [The OpenAPI](./docs/index.html) doc for information on the API and Data Structures Used. 

This system uses the [Flask]() API framework, and the [Echo](./ECHO.md) discord chat agent framework.

# Separation of Concerns

Folder structure for source code
```
/src
| /agents         ECHO Agent Implementations
| /config         Implements, global configuration management
| /echo           Implements the Echo chat agent framework
| /echo_utils     Stage0 Echo helpers
| /flask_utils    Stage0 Flask helpers
| /mongo_utils    Simple Mongo IO Wrapper
| /routes         Flask route implementations
| /services       Business Service implementations 
                   (support routes and agents)
```

Note: /echo and bot & conversation agents/routes/services will be extracted to an Echo package. The config, config agents/routes, and *_utils folders will be extracted to stage0_api_utilities package. This will leave only agents, routes, services in this repo.

# Supported pipenv commands
- ``pipenv run local`` run the server locally in dev mode
- ``pipenv run start`` restart the backing database and run locally *TODO
- ``pipenv run test`` run unittest testing
- ``pipenv run stepci`` run stepci testing
- ``pipenv run build`` build container locally 
- ``pipenv run container`` build and run container
