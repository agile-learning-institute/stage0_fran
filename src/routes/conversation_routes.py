from echo.message import Message
from flask_utils.breadcrumb import create_breadcrumb
from flask_utils.token import create_token
from services.conversation_services import ConversationServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for conversation routes
def create_conversation_routes():
    conversation_routes = Blueprint('conversation_routes', __name__)

    # GET /api/conversations - Return a list of latest active conversations
    @conversation_routes.route('', methods=['GET'])
    def get_conversations():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversations = ConversationServices.get_conversations(token=token)
            logger.debug(f"get_conversations Success {breadcrumb}")
            return jsonify(conversations), 200
        except Exception as e:
            logger.warning(f"get_conversations Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/conversation/channel_id - Return a specific conversation
    @conversation_routes.route('/<string:channel_id>', methods=['GET'])
    def get_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.get_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
            logger.debug(f"get_conversation Success {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"get_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/conversation/{channel_id} - Update a conversation
    @conversation_routes.route('/<string:channel_id>', methods=['PATCH'])
    def update_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.update_conversation(channel_id=channel_id, data=data, token=token, breadcrumb=breadcrumb)
            logger.debug(f"update_conversation Successful {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"update_conversation processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/{channel_id}/message - Add a message to a conversation
    @conversation_routes.route('/<string:channel_id>/message', methods=['POST'])
    def add_message(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            message = Message(llm_message=request.get_json(), user=token["user_id"])
            messages = ConversationServices.add_message(channel_id=channel_id, message=message.as_llm_message(), token=token, breadcrumb=breadcrumb)
            logger.debug(f"add_message Successful {breadcrumb}")
            return jsonify(messages), 200
        except Exception as e:
            logger.warning(f"add_message processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/{channel_id}/reset - Reset the currently active conversation 
    @conversation_routes.route('/<string:channel_id>/reset', methods=['POST'])
    def reset_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            messages = ConversationServices.reset_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
            logger.debug(f"reset_conversation successful {breadcrumb}")
            return jsonify(messages), 200
        except Exception as e:
            logger.warning(f"reset_conversation processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    logger.info("Conversation Flask Routes Registered")
    return conversation_routes