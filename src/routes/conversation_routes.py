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
            logger.info(f"Get conversation Success {breadcrumb}")
            return jsonify(conversations), 200
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/conversation/channel_id - Return a specific conversation
    @conversation_routes.route('/<string:channel_id>', methods=['GET'])
    def get_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = ConversationServices.get_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
            logger.info(f"Get conversation Success {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/conversation/{channel_id} - Update a conversation
    @conversation_routes.route('/<string:channel_id>', methods=['PATCH'])
    def update_conversation(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.update_conversation(channel_id=channel_id, data=data, token=token, breadcrumb=breadcrumb)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/{channel_id}/message - Add a message to a conversation
    @conversation_routes.route('/<string:channel_id>/message', methods=['POST'])
    def add_message(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            message = request.data.decode('utf-8')
            logger.info(f"add_message route channel_id={channel_id}, message={message}")
            messages = ConversationServices.add_message(channel_id=channel_id, message=message, token=token, breadcrumb=breadcrumb)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return jsonify(messages), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return conversation_routes