# stage0_fran
Fran the Facilitator Discord Bot

```yaml
Commands:
-   command: schedule_workshop
    input_schema:
    description: Schedule Info
        type: object
        properties:
            name:
                description: Workshop Name
                type: Sentence
            purpose:
                description: Workshop Purpose
                type: Paragraph
            when:
                description: Date/Time for the Workshop Event
                type: Appointment (Date/Time From/To)
            status:
                description: Status
                type: enum[Pending, Active, Complete]
            chain:
                description: Chain to use as workshop template
                type: word
            users:
                description: List of users to attend workshop event
                type: array
    reply_schema:
        description: Simple acknowledgement of id or error
        type: object
        properties:
            _id:
                description: The ID (channel name) of the workshop created
                type: ID
            err:
                description: Error message if workshop was not created.
                type: Sentence

- command: get_workshop
    input_schema:
    description: Workshop Identifier
    type: object
    properties:
        product_id:
        workshop_id:
    reply_schema:
    description: Workshop Object
    type: object
    properties:

- command: get_workshop_exercise
    input_schema:
    description: Workshop Identifier
    type: object
    properties:
        product_id:
        workshop_id:
        exercise_index:
    reply_schema:
    description: Exercise Object
    type: object
    properties:

- command: patch_workshop
    input_schema:
    description: Workshop Object
    type: object
    properties:
    reply_schema:
    description: Workshop Object
    type: object
    properties:

- command: add_workshop_observation
    input_schema:
    description: Observation Object
    type: object
    properties:
    reply_schema:
    description: Simple acknowledgment
    type: string

- command: get exercises
    input_schema:
- command: get exercise
    input_schema:
- command: get chains
    input_schema:
- command: get chain
    input_schema:
```



Commands

Schedule Workshop
- Collect user names (id's) that will attend
- Get the workshop design chain
- Get the date/time
- Get the channel name
- Action: Create Channel, Post welcome message

Start Workshop

/src
| /server.py - Initialize the server, Discord client, Inference client, And database connections
| /config/config.py - Implements, global configuration values
| /routes (http code)
| | /config_routes.py - Observability Endpoint
| | /workshop_routes.py 
| | /exercise_routes.py
| | /chain_routes.py 
| /handlers (bot handlers)
| | /fran_handlers.py - Bot event handlers for Fran channel
| | /workshop_handlers.py - Bot event handlers for Workshop channel
| /services (business logic, supports handlers/routes, uses io_utils)
| | /workshop_services.py
| | /exercise_services.py
| | /chain_services.py
| /io_utils
| | /inference.py - Simple LLM Wrapper
| | /mongo.py - Simple Mongo IO Wrapper
/models - ollama model files
| /Fran.modelfile - Generalist design thinking model
| /Fran.{exercise}.modelfile - Specialized model for exercise specific conversations.
# Discord Design Thinking Workshop
