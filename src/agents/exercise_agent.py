import logging
from echo import Blueprint
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from services.exercise_services import ExerciseServices

logger = logging.getLogger(__name__)

def create_exercise_agent():
    """ Registers event handlers and commands for the Fran home channel. """
    exercise_agent = Blueprint('conversation_agent', __name__)
    
    @exercise_agent.action(action_name="get_exercises", 
                description="Return a list of active exercises", 
                arguments_schema={},
                outputs_schema={
                    "description": "List of name and id's of all exercises",
                    "type": "array",
                    "items": {
                        "type":"object",
                        "properties": {
                            "_id": {
                                "description": "",
                                "type": "unique identifier",
                            },
                            "name": {
                                "description": "",
                                "type": "string",
                            },
                        }
                    }
                })
    async def get_exercises(arguments):
        """ Slash command to get a list of all active exercises"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            exercises = ExerciseServices.get_exercises(token)
            logger.info(f"Get Exercise Success {breadcrumb}")
            return exercises
        except Exception as e:
            logger.warning(f"Get Exercise Action Error has occurred: {e}")
            return "A processing error occurred"

    @exercise_agent.action(action_name="get_exercise", 
        description="Get a specific exercise", 
        arguments_schema={
            "description": "Exercise unique identifier (from get_exercises)",
            "type": "identifier",
        },
        outputs_schema={
            "title": "Exercise",
            "description": "A description of the exercise, and instructions on how to guide it.",
            "type": "object",
            "properties": {
                "_id": {
                    "description": "The unique identifier for a Exercise",
                    "type": "identifier"
                },
                "status": {
                    "description": "The status of the Exercise Record",
                    "type": "enum",
                    "enums": "default_status"
                },
                "name": {
                    "description": "Short name for the exercise",
                    "type": "word"
                },
                "description": {
                    "description": "A description of the exercise and when to use it",
                    "type": "paragraph"
                },
                "duration": {
                    "description": "duration in minutes",
                    "type": "count"
                },
                "observe_instructions": {
                    "description": "observation exercise instructions",
                    "type": "markdown"
                },
                "reflect_instructions": {
                    "description": "reflect exercise instructions",
                    "type": "markdown"
                },
                "make_instructions": {
                    "description": "make exercise instructions",
                    "type": "markdown"
                },
                "last_saved": {
                    "description": "Last Saved breadcrumb",
                    "type": "breadcrumb"
                }
            }
        }
    )
    async def get_exercise(arguments):
        """ Slash command to get a specific exercises"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            exercises = ExerciseServices.get_exercises(token)
            logger.info(f"Get Exercise Success {breadcrumb}")
            return exercises
        except Exception as e:
            logger.warning(f"Get Exercise Action Error has occurred: {e}")
            return "A processing error occurred"
