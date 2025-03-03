from flask import Blueprint, jsonify
from src.flask_utils.breadcrumb import create_breadcrumb
from src.flask_utils.token import create_token
from src.config.config import Config

import logging
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_echo_routes(agents=None):
    echo_routes = Blueprint('echo_routes', __name__)
    agents = agents or {}
    
    # GET /api/echo - Return the agents
    @echo_routes.route('', methods=['GET'])
    def get_agents():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            logger.debug(f"get_agents Success {breadcrumb}")
            return jsonify(agents), 200
        except Exception as e:
            logger.warning(f"get_agents Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return echo_routes