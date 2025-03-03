from src.flask_utils.breadcrumb import create_breadcrumb
from src.flask_utils.token import create_token
from src.services.chain_services import ChainServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for chain routes
def create_chain_routes():
    chain_routes = Blueprint('chain_routes', __name__)

    # GET /api/chain - Return a list of chains that match query
    @chain_routes.route('', methods=['GET'])
    def get_chains():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            chains = ChainServices.get_chains(token=token)
            logger.debug(f"get_chains Success {breadcrumb}")
            return jsonify(chains), 200
        except Exception as e:
            logger.warning(f"get_chains Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/chain/{id} - Return a specific chain
    @chain_routes.route('/<string:id>', methods=['GET'])
    def get_chain(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            chain = ChainServices.get_chain(chain_id=id, token=token)
            logger.debug(f"get_chain Success {breadcrumb}")
            return jsonify(chain), 200
        except Exception as e:
            logger.warning(f"get_chain Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return chain_routes