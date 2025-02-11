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


/src
| /server.py - Initialize the server, Discord client, Inference client, And database connections
| /config/config.py - Implements, global configuration values
| /echo/Echo.py - Echo flask-like chat agent framework
| /agents - ChatBot Agent handlers
| | /config_agent.py
| | /chain_agent.py
| | /exercise_agent.py
| | /workshop_agent.py
| |
| /routes - Http Event handlers
| | /config_routes.py
| | /chain_routes.py
| | /exercise_routes.py
| | /workshop_routes.py
| |
| /services - Business logic, supports agents/routes, uses io_utils
| | /chain_services.py
| | /exercise_services.py
| | /workshop_services.py
| |
| /flask_utils - Flask helpers
| /llm_utils - LLM Wrapper
| /mongo_utils - Simple Mongo IO Wrapper
|
/models - ollama model files
| /Fran.modelfile - Generalist design thinking model
| /Fran.{exercise}.modelfile - Specialized model for exercise specific conversations.
