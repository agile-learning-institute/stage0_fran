from flask_utils.breadcrumb import create_breadcrumb
from flask_utils.token import create_token
from services.conversation_services import conversationServices

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
            conversations = conversationServices.get_conversations(query, token)
            logger.info(f"Get conversation Success {breadcrumb}")
            return jsonify(conversations), 200
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/conversation/id - Return a specific conversation
    @conversation_routes.route('/<string:id>', methods=['GET'])
    def get_conversation(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            conversation = conversationServices.get_conversation(id, token)
            logger.info(f"Get conversation Success {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"Get conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/conversation/{id} - Update a conversation
    @conversation_routes.route('/<string:id>', methods=['PATCH'])
    def update_conversation(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            patch_data = request.get_json()
            conversation = conversationServices.update_conversation(id, token, breadcrumb, patch_data)
            logger.info(f"Update conversation Successful {breadcrumb}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return conversation_routes