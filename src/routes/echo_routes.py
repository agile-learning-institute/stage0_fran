from flask import Blueprint, jsonify
from flask_utils.breadcrumb import create_breadcrumb
from flask_utils.token import create_token
from echo.echo import Echo

import logging
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_echo_routes(echo=None):
    echo_routes = Blueprint('echo_routes', __name__)
    if not isinstance(echo, Echo):
        raise Exception("create_echo_routes Error: an instance of Echo is a required parameter")
    
    # GET /api/echo - Return the agents
    @echo_routes.route('', methods=['GET'])
    def get_agents():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            logger.debug(f"get_agents Success {breadcrumb}")
            agents = echo.get_agents()
            return jsonify(agents), 200
        except Exception as e:
            logger.warning(f"get_agents {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/echo - Return the agents
    @echo_routes.route('/<string:name>', methods=['GET'])
    def get_agent(name):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            agent = echo.get_agent(agent_name=name)
            logger.debug(f"get_agent Success {breadcrumb}")
            return jsonify(agent), 200
        except Exception as e:
            logger.warning(f"get_agent {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return echo_routes