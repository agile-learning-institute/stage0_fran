import logging
from stage0_py_utils import Agent, create_echo_breadcrumb, create_echo_token
from stage0_fran.services.workshop_services import WorkshopServices

logger = logging.getLogger(__name__)

def create_workshop_agent(agent_name):
    """ Registers agent actions for Echo agent."""
    agent = Agent(agent_name)
    
    # Define reused schema's
    workshop_schema = {
        "title": "Workshop",
        "description": "A record of a specific design thinking workshop.",
        "type": "object",
        "properties": {
            "_id": {
                "description": "The unique identifier for a Workshop",
                "type": "identifier"
            },
            "status": {
                "description": "Workshop Status/State",
                "type": "enum",
                "enums": "workshop_status"
            },
            "channel_id": {
                "description": "The discord identifier for the channel this workshop is hosted on",
                "type": "identifier"
            },
            "channel_name": {
                "description": "Workshop Name (Channel Name)",
                "type": "word"
            },
            "category": {
                "description": "Discord Channel Category where this workshop channel is",
                "type": "sentence"
            },
            "guild": {
                "description": "Discord Server where this workshop takes place",
                "type": "sentence"
            },
            "purpose": {
                "description": "Workshop Purpose",
                "type": "paragraph"
            },
            "when": {
                "description": "From-To Date/Time for the Workshop Event",
                "type": "appointment"
            },
            "current_exercise": {
                "description": "Index of the current exercise for Active workshops",
                "type": "index"
            },
            "exercises": {
                "description": "List of workshop_exercise documents",
                "type": "array",
                "items": {
                    "description": "A reference to a Workshop Exercise",
                    "type": "object",
                    "properties": {
                        "exercise_id": {
                            "description": "The Exercise Instructions this is using",
                            "type": "identifier"
                        },
                        "status": {
                            "description": "The exercise status or state (Observe/Reflect/Make)",
                            "type": "enum",
                            "enums": "exercise_status"
                        },
                        "workshop_id": {
                            "description": "The _id of the workshop for this exercise",
                            "type": "identifier"
                        }
                    }
                }   
            },
            "last_saved": {
                "description": "Last Saved breadcrumb",
                "type": "breadcrumb"
            }
        }
    }
    
    def get_workshops(arguments):
        """ """
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshops = WorkshopServices.get_workshops(query=arguments, token=token)
            logger.info(f"Get workshops Success")
            return workshops
        except Exception as e:
            logger.warning(f"Get workshops Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_workshops",
        function=get_workshops,
        description="Return a list of active, latests, workshops", 
        arguments_schema={
            "description": "Query String Regex to match name"
        },
        output_schema={
            "description": "List of name and id's of workshops that match the query",
            "type": "array",
            "items": {
                "type":"object",
                "properties": {
                    "_id": {
                        "description": "",
                        "type": "unique identifier",
                    },
                    "name": {
                        "description": "",
                        "type": "string",
                    },
                }
            }
        })

    def get_workshop(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshop = WorkshopServices.get_workshop(workshop_id=arguments, token=token)
            logger.info(f"Get workshop Success")
            return workshop
        except Exception as e:
            logger.warning(f"Get workshop Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_workshop", 
        function=get_workshop,
        description="Get a workshop by ID", 
        arguments_schema={
            "description":"Workshop Identifier. Use get_workshops to find identifiers by name",
            "type": "string", 
        },
        output_schema=workshop_schema
    )

    def add_workshop(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshop = WorkshopServices.add_workshop(
                chain_id=arguments["chain"], 
                data=arguments["workshop"], 
                token=token, breadcrumb=breadcrumb
            )
            logger.info(f"add_workshop Successful {str(breadcrumb["correlationId"])}")
            return workshop
        except Exception as e:
            logger.warning(f"add_workshop Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="add_workshop", 
        function=add_workshop,
        description="Create the specified workshop", 
        arguments_schema= {
            "description": "add_workshop arguments",
            "type": "object",
            "properties": {
                "chain": {
                    "description": "Chain ID to use when initializing the workshop",
                    "type": "string"
                },
                "workshop": workshop_schema
            }
        },
        output_schema=workshop_schema
    )
        
    def update_workshop(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshop = WorkshopServices.update_workshop(
                workshop_id=arguments["_id"], 
                workshop=arguments, 
                token=token, breadcrumb=breadcrumb)
            logger.info(f"update_workshop Successful {str(breadcrumb["correlationId"])}")
            return workshop
        except Exception as e:
            logger.warning(f"update_workshop Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="update_workshop", 
        function=update_workshop,
        description="Update the specified workshop", 
        arguments_schema=workshop_schema,
        output_schema=workshop_schema
    )
        
    def start_workshop(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshop = WorkshopServices.start_workshop(
                workshop_id=arguments,
                token=token, breadcrumb=breadcrumb
            )
            logger.info(f"start_workshop Successful {str(breadcrumb["correlationId"])}")
            return workshop
        except Exception as e:
            logger.warning(f"start_workshop Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="start_workshop", 
        function=start_workshop,
        description="Set the workshop to active status.", 
        arguments_schema= {
            "description": "workshop_id",
            "type": "string"
        },
        output_schema={    
            "description":"The workshop after update",
            "type": workshop_schema
        })

    def advance_workshop(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            workshop = WorkshopServices.advance_workshop(
                workshop_id=arguments,
                token=token, breadcrumb=breadcrumb
            )
            logger.info(f"advance_workshop Successful {str(breadcrumb["correlationId"])}")
            return workshop
        except Exception as e:
            logger.warning(f"advance_workshop Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="advance_workshop", 
        function=advance_workshop,
        description="Advance the current exercise and update status as needed", 
        arguments_schema= {
            "description": "workshop_id",
            "type": "string"
        },
        output_schema={    
            "description":"The workshop after update",
            "type": workshop_schema
        })

    def add_observation(arguments):
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            messages = WorkshopServices.add_observation(
                workshop_id=arguments["workshop_id"],
                observation=arguments["observation"], 
                token=token, breadcrumb=breadcrumb
            )
            logger.info(f"add_observation Successful {str(breadcrumb["correlationId"])}")
            return messages
        except Exception as e:
            logger.warning(f"add_observation Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="add_observation", 
        function=add_observation,
        description="Add a message to the specified workshop", 
        arguments_schema= {
            "description": "add_observation arguments",
            "type": "object",
            "properties": {
                "workshop_id": {
                    "description": "Chain ID to use when initializing the workshop",
                    "type": "string"
                },
                "observation": {
                    "description": "An observation workshop",
                    "type": "object"
                }
            }
        },
        output_schema={    
            "description":"The workshop after update",
            "type": workshop_schema
        })
        
    logger.info("Registered agent agent action handlers.")
    return agent