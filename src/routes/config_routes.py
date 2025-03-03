from flask import Blueprint, jsonify
from src.flask_utils.breadcrumb import create_breadcrumb
from src.flask_utils.token import create_token
from src.config.config import Config

import logging
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_config_routes():
    config_routes = Blueprint('config_routes', __name__)
    config = Config.get_instance()
    
    # GET /api/config - Return the current configuration as JSON
    @config_routes.route('', methods=['GET'])
    def get_config():
        try:
            # Return the JSON representation of the config object
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            logger.debug(f"get_config Success {breadcrumb}")
            return jsonify(config.to_dict(token)), 200
        except Exception as e:
            logger.warning(f"get_config Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    logger.info("Config Flask Routes Registered")
    return config_routes