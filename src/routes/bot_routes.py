from src.flask_utils.breadcrumb import create_breadcrumb
from src.flask_utils.token import create_token
from src.services.bot_services import BotServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for bot routes
def create_bot_routes():
    bot_routes = Blueprint('bot_routes', __name__)

    # GET /api/bots - Return a list of bots that match query
    @bot_routes.route('', methods=['GET'])
    async def get_bots():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            bots = await BotServices.get_bots(query, token)
            logger.info(f"Get bot Success {breadcrumb}")
            return jsonify(bots), 200
        except Exception as e:
            logger.warning(f"Get bot Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/bot/{id} - Return a specific bot
    @bot_routes.route('/<string:id>', methods=['GET'])
    async def get_bot(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            bot = await BotServices.get_bot(id, token)
            logger.info(f"Got Bot: {bot}")
            logger.info(f"Get bot Success {breadcrumb}")
            return jsonify(bot), 200
        except Exception as e:
            logger.warning(f"Get bot Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/bot/{id} - Update a bot
    @bot_routes.route('/<string:id>', methods=['PATCH'])
    async def update_bot(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            patch_data = request.get_json()
            bot = await BotServices.update_bot(id, token, breadcrumb, patch_data)
            logger.info(f"Update bot Successful {breadcrumb}")
            logger.info(f"Got bot {bot}")
            return jsonify(bot), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/bot/{id}/channels - Get Active Channels
    @bot_routes.route('/<string:id>/channels', methods=['GET'])
    async def get_channels(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            channels = await BotServices.get_channels(id, token, breadcrumb)
            logger.info(f"Get Channels from Bot Successful {breadcrumb}")
            return jsonify(channels), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # POST /api/bot/{id}/channel/{channel_id} - Add a channel
    @bot_routes.route('/<string:id>/channel/<string:channel_id>', methods=['POST'])
    async def add_channel(id, channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            channels = await BotServices.add_channel(id, token, breadcrumb, channel_id)
            logger.info(f"Add Channel to Bot Successful {breadcrumb}")
            return jsonify(channels), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # DELETE /api/bot/{id}/channel/{channel_id} - Remove a channel
    @bot_routes.route('/<string:id>/channel/<string:channel_id>', methods=['DELETE'])
    async def remove_channel(id, channel_id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            channels = await BotServices.remove_channel(id, token, breadcrumb, channel_id)
            logger.info(f"Add Channel to Bot Successful {breadcrumb}")
            return jsonify(channels), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # Ensure the Blueprint is returned correctly
    return bot_routes