from src.flask_utils import create_breadcrumb, create_token
from src.services.chain_services import ChainServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for chain routes
def create_chain_routes():
    chain_routes = Blueprint('chain_routes', __name__)

    # GET /api/chains - Return a list of chains that match query
    @chain_routes.route('s', methods=['GET'])
    def get_chains():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            chains = ChainServices.get_chains(query, token)
            logger.info(f"Get Chain Success {breadcrumb}")
            return jsonify(chains), 200
        except Exception as e:
            logger.warning(f"Get Chain Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/chain/id - Return a specific chain
    @chain_routes.route('/<string:id>', methods=['GET'])
    def get_Chain(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            chain = ChainServices.get_chain(id, token)
            logger.info(f"Get Chain Success {breadcrumb}")
            return jsonify(chain), 200
        except Exception as e:
            logger.warning(f"Get Chain Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/chain/{id} - Update a chain
    @chain_routes.route('/<string:id>', methods=['PATCH'])
    def update_chain(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            patch_data = request.get_json()
            chain = ChainServices.update_chain(id, token, breadcrumb, patch_data)
            logger.info(f"Update Chain Successful {breadcrumb}")
            return jsonify(chain), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return chain_routes