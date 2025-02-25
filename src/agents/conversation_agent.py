import logging
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from echo.agent import Agent
from services.conversation_services import ConversationServices

logger = logging.getLogger(__name__)

def create_conversation_agent(agent_name):
    """ Registers agent actions for Echo agent."""
    agent = Agent(agent_name)
    
    # Define reused schema's
    conversation_schema = {
        "description": "A conversation with a list of messages",
        "type": "object",
        "properties": {
            "_id": {
                "description": "The unique identifier for a conversation mongo document",
                "type": "identifier"
            },
            "status": {
                "description": "The unique identifier for a conversation mongo document",
                "type": "string",
                "enum": ["Active", "Archived"]
            },
            "channel_id": {
                "description": "The Discord channel_id this conversation is taking place in",
                "type": "string"
            },
            "version": {
                "description": "Either 'latest' or the date the conversation was archived",
                "type": "string"
            },
            "conversation": {
                "description": "Messages in the conversation",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "last_saved": {
                "description": "Last Saved tracking breadcrumb",
                "type": "breadcrumb"
            }
        }
    }
    
    def get_conversations(arguments):
        """ """
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversations = ConversationServices.get_conversations(token=token)
            logger.info(f"Get conversations Success {breadcrumb}")
            return conversations
        except Exception as e:
            logger.warning(f"Get conversations Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_conversations",
        function=get_conversations,
        description="Return a list of active, latests, conversations", 
        arguments_schema={"none"},
        output_schema={
            "description": "List of name and id's of conversations that match the query",
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

    def get_conversation(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.get_conversation(channel_id=arguments, token=token)
            logger.info(f"Get conversation Success {breadcrumb}")
            return conversation
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_conversation", 
        function=get_conversation,
        description="Get a conversation by ID", 
        arguments_schema={
            "description":"Channel Identifier",
            "type": "string", 
        },
        output_schema=conversation_schema
    )

    def update_conversation(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.update_conversation(
                channel_id=arguments["channel_id"], 
                conversation=arguments, 
                token=token, breadcrumb=breadcrumb)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return conversation
        except Exception as e:
            logger.warning(f"Update conversation Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="update_conversation", 
        function=update_conversation,
        description="Update the specified conversation", 
        arguments_schema=conversation_schema,
        output_schema=conversation_schema
    )
        
    def add_message(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            messages = ConversationServices.add_message(
                channel_id=arguments["channel_id"],
                message=arguments["message"], 
                token=token, breadcrumb=breadcrumb)
            logger.info(f"Add Message Successful {breadcrumb}")
            return messages
        except Exception as e:
            logger.warning(f"Add Message Error has occurred {e}")
            return "error"
    agent.register_action(
        action_name="add_message", 
        function=add_message,
        description="Add a message to the specified conversation", 
        arguments_schema={
            "description":"A channel_id and the message to add",
            "type": "object", 
            "properties": {
                "channel_id": {
                    "description": "",
                    "type": "string"
                },
                "message": {
                    "description": "",
                    "type": "string"
                }                
            }
        },
        output_schema={    
            "description":"The new message in the conversational context",
            "type": "array", 
            "items": {
                "description": "A message in the conversation",
                "type": "string"
            }
        })
        
    logger.info("Registered agent agent action handlers.")
    return agent