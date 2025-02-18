from src.flask_utils.breadcrumb import create_breadcrumb
from src.flask_utils.token import create_token
from src.services.exercise_services import ExerciseServices

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for exercise routes
def create_exercise_routes():
    exercise_routes = Blueprint('exercise_routes', __name__)

    # GET /api/exercise - Return a list of exercises that match query
    @exercise_routes.route('', methods=['GET'])
    def get_exercises():
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            query = request.args.get('query') or ""
            exercises = ExerciseServices.get_exercises(token)
            logger.info(f"Get Exercise Success {breadcrumb}")
            return jsonify(exercises), 200
        except Exception as e:
            logger.warning(f"Get Exercise Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/exercise/id - Return a specific exercise
    @exercise_routes.route('/<string:id>', methods=['GET'])
    def get_Exercise(id):
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            exercise = ExerciseServices.get_exercise(id, token)
            logger.info(f"Get exercise Success {breadcrumb}")
            return jsonify(exercise), 200
        except Exception as e:
            logger.warning(f"Get Exercise Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # Ensure the Blueprint is returned correctly
    return exercise_routes