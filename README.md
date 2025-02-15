# stage0_fran

This repository contains the API that supports the user interface for creating, conducting, and recording Design Thinking workshops for stage0. This API is also served as a collection of chat agents through a discord chat-bot framework. 

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
/src
| /server.py - Initialize the server, Discord client, Inference client, And database connections
| /config - Implements, global configuration values, to be extracted to stage0_api_utils private package
| /echo/Echo.py - Echo flask-like chat agent framework, to be extracted to Echo public package
| /agents - ChatBot Agent handlers
| /routes - Http Event handlers
| /services - Business logic, supports agents/routes, uses *_utils
| /flask_utils - Flask helpers, to be extracted to stage0_api_utils private package
| /llm_utils - LLM Wrapper, to be extracted to stage0_api_utils private package
| /mongo_utils - Simple Mongo IO Wrapper, to be extracted to stage0_api_utils private package
|
/Fran.modelfile - Generalist design thinking model
