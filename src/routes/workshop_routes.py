from flask_utils.breadcrumb import create_breadcrumb
from flask_utils.token import create_token
from services.workshop_services import WorkshopServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for workshop routes
def create_workshop_routes():
    workshop_routes = Blueprint('workshop_routes', __name__)

    # GET /api/workshop - Return a list of workshops that match query
    @workshop_routes.route('', methods=['GET'])
    def get_workshops():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            workshops = WorkshopServices.get_workshops(query, token)
            logger.info(f"Get workshops Success {query} {breadcrumb}")   
            return jsonify(workshops), 200
        except Exception as e:
            logger.warning(f"Get workshops Error has occurred: {e}")
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

    # POST /api/workshop/new/{chain} - Add a new workshop from the chain
    @workshop_routes.route('new/<string:chain>', methods=['POST'])
    def add_workshop(chain):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop_data = request.get_json()
            workshop = WorkshopServices.add_workshop(chain, workshop_data, token, breadcrumb)
            logger.info(f"add_workshop Success {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"add_workshop Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # PATCH /api/workshop/{id} - Update a workshop
    @workshop_routes.route('/<string:id>', methods=['PATCH'])
    def update_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            patch_data = request.get_json()
            workshop = WorkshopServices.update_workshop(id, patch_data, token, breadcrumb)
            logger.info(f"Update workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"update_workshop A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/workshop/{id}/start - Update a workshop status
    @workshop_routes.route('/<string:id>/start', methods=['POST'])
    def start_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop = WorkshopServices.start_workshop(id, token, breadcrumb)
            logger.info(f"Start workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"start_workshop A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/workshop/{id}/next - Update a workshop, advance current_exercise
    @workshop_routes.route('/<string:id>/next', methods=['POST'])
    def advance_workshop(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            workshop = WorkshopServices.advance_workshop(id, token, breadcrumb)
            logger.info(f"Advance workshop Successful {breadcrumb}")
            return jsonify(workshop), 200
        except Exception as e:
            logger.warning(f"advance_workshop A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/workshop/{id}/observation - Add a observation to a workshop
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
            logger.warning(f"add_observation A processing error occurred {e}")
            return jsonify({"error": "A processing error occurred"}), 500
                
    # Ensure the Blueprint is returned correctly
    return workshop_routes