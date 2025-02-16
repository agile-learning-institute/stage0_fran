import json
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from services.conversation_services import ConversationServices

import logging
logger = logging.getLogger(__name__)

from echo import Blueprint, Message

# Define the Blueprint for conversation routes
def create_conversation_agent():
    conversation_agent = Blueprint('conversation_agent', __name__)

    @conversation_agent.action(action_name="get_conversations", 
                description="Return a list of conversations that optionally match query", 
                arguments_schema={
                    "description":"Request Query String to be found in name",
                    "type": "object", 
                    "properties": {
                        "query": {
                            "description": "",
                            "type": "string"
                        }
                    }
                },
                outputs_schema={
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
    def get_conversations(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = arguments['query'] or ""
            conversations = ConversationServices.get_conversations(query, token)
            logger.info(f"Get conversation Success {breadcrumb}")
            return json.dumps(conversations, separators=(',', ':'))
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return '{"error": "A processing error occurred"'
        
    @conversation_agent.action(action_name="get_conversation", 
                description="Get a conversation by ID", 
                arguments_schema={
                    "description":"Discord Channel Identifier",
                    "type": "string", 
                },
                outputs_schema={
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
                })
    def get_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.get_conversation(channel_id, token)
            logger.info(f"Get conversation Success {breadcrumb}")
            return json.dumps(conversation)
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return json.dumps({"error": "A processing error occurred"})

    @conversation_agent.action(action_name="update_conversation", 
                description="Update the specified conversation", 
                arguments_schema={
                },
                outputs_schema={
                })
    def update_conversation(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.update_conversation(arguments.channel_id, token, breadcrumb, arguments.patch_data)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return json.dumps(conversation)
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return json.dumps({"error": "A processing error occurred"})
        
    @conversation_agent.action(action_name="add_message", 
                description="Add a message to the specified conversation", 
                arguments_schema={
                },
                outputs_schema={
                })
    def add_message(arguments):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.add_message(arguments.channel_id, token, breadcrumb, arguments.message)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return json.dumps(conversation)
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return json.dumps({"error": "A processing error occurred"})
        
    # Ensure the Blueprint is returned correctly
    return conversation_agent