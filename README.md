# stage0_fran

This repository contains the API and Discord Chatbot that supports the user interface for creating, conducting, and recording Design Thinking workshops for stage0. This API is also served as a chat agent through a discord chat-bot framework. 

See [The OpenAPI](./docs/index.html) doc for information on the API and Data Structures Used. 

This system uses the [Echo] package to expose agent actions in a discord chat conversation.

# Separation of Concerns

### Code designed to be extracted to a Echo package.
This is a Flask-like Package for Discord Bots
```
/src
| /echo/Echo.py - Echo flask-like chat agent framework
```

### Code designed to be extracted to a stage0_utils package.
This shared code will be used in all of the stage0 Bot's and API's
```
/src
| /config - Implements, global configuration management
| /flask_utils - Flask helpers
| /llm_utils - LLM Wrapper
| /mongo_utils - Simple Mongo IO Wrapper
| /echo_utils - conversation_[agent, route, service]
```

### Code specific to the Fran API
```
/src
| /server.py - Initialize the server, connect to backing services
| /agents - Echo Agent handlers
| /routes - Flask endpoint handlers
| /services - Business logic, supports agents and routes
```

# Supported pipenv commands
- ``pipenv run local`` run the server locally in dev mode
- ``pipenv run start`` restart the backing database and run locally *TODO
- ``pipenv run test`` run unittest testing
- ``pipenv run stepci`` run stepci testing
- ``pipenv run build`` build container locally 
- ``pipenv run container`` build and run container
