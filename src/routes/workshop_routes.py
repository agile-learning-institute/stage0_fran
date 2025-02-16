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
        
    # POST /api/workshop - Add a new workshop
    @workshop_routes.route('', methods=['GET'])
    def add_workshop():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop_data = request.get_json()
            workshop = WorkshopServices.create_workshop(workshop_data, token)
            logger.info(f"Get workshop Success {breadcrumb}")
            return jsonify(workshop), 200
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
        
    # POST /api/workshop/{id}/start - Update a workshop
    @workshop_routes.route('/<string:id>/start', methods=['POST'])
    def start_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop = WorkshopServices.start_workshop(id, token, breadcrumb)
            logger.info(f"Start workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/workshop/{id}/next - Update a workshop
    @workshop_routes.route('/<string:id>/next', methods=['POST'])
    def advance_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop = WorkshopServices.advance_workshop(id, token, breadcrumb)
            logger.info(f"Advance workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/workshop/{id}/observation - Update a workshop
    @workshop_routes.route('/<string:id>/observation', methods=['POST'])
    def add_observation(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            observation = request.get_json()
            workshop = WorkshopServices.add_observation(id, token, breadcrumb, observation)
            logger.info(f"Add observation to workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # PATCH /api/workshop/{id}/observation - Update a workshop
    @workshop_routes.route('/<string:id>/observation', methods=['PATCH'])
    def add_observation(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            observations = request.get_json()
            workshop = WorkshopServices.update_observations(id, token, breadcrumb, observations)
            logger.info(f"Update workshop observations Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # Ensure the Blueprint is returned correctly
    return workshop_routes