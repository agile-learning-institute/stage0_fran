from flask_utils.breadcrumb import create_breadcrumb
from flask_utils.token import create_token
from services.conversation_services import ConversationServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for conversation routes
def create_conversation_routes():
    conversation_routes = Blueprint('conversation_routes', __name__)

    # GET /api/conversations - Return a list of conversations that match query
    @conversation_routes.route('s', methods=['GET'])
    def get_conversations():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            conversations = ConversationServices.get_conversations(query, token)
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
            conversation = ConversationServices.get_conversation(channel_id, token)
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
            patch_data = request.get_json()
            conversation = ConversationServices.update_conversation(channel_id, token, breadcrumb, patch_data)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/{channel_id}/message - Update a conversation
    @conversation_routes.route('/<string:channel_id>/message', methods=['POST'])
    def add_message(channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            message = request.json
            conversation = ConversationServices.add_message(channel_id, token, breadcrumb, message)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return conversation_routes