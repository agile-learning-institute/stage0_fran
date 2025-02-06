from src.flask_utils import create_breadcrumb, create_token
from src.services.workshop_services import WorkshopServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for workshop routes
def create_workshop_routes():
    workshop_routes = Blueprint('workshop_routes', __name__)

    # GET /api/workshops - Return a list of workshops that match query
    @workshop_routes.route('s', methods=['GET'])
    def get_workshops():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            workshops = WorkshopServices.get_workshops(query, token)
            logger.info(f"Get workshop Success {breadcrumb}")
            return jsonify(workshops), 200
        except Exception as e:
            logger.warning(f"Get workshop Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/workshop/id - Return a specific workshop
    @workshop_routes.route('/<string:id>', methods=['GET'])
    def get_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop = WorkshopServices.get_workshop(id, token)
            logger.info(f"Get workshop Success {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"Get workshop Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PATCH /api/workshop/{id} - Update a workshop
    @workshop_routes.route('/<string:id>', methods=['PATCH'])
    def update_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            patch_data = request.get_json()
            workshop = WorkshopServices.update_workshop(id, token, breadcrumb, patch_data)
            logger.info(f"Update workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return workshop_routes