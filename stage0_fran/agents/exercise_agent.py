import logging
from stage0_py_utils import Agent, create_echo_token, create_echo_breadcrumb
from stage0_fran.services.exercise_services import ExerciseServices

logger = logging.getLogger(__name__)

def create_exercise_agent(agent_name):
    """ Registers event handlers and commands for the Fran home channel. """
    agent = Agent(agent_name)
    
    def get_exercises(arguments):
        """Get the list of Exercise Names and IDs"""
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            exercise = ExerciseServices.get_exercises(token=token)
            logger.info(f"get_exercises Successful {str(breadcrumb["correlationId"])}")
            return exercise
        except Exception as e:
            logger.warning(f"A get_exercises Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_exercises", 
        function=get_exercises,
        description="Return a list of active exercises", 
        arguments_schema="none",
        output_schema={
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

    def get_exercise(arguments):
        """Get a specific exercise exercise"""
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            exercise = ExerciseServices.get_exercise(exercise_id=arguments, token=token)
            logger.info(f"get_exercise Successful {str(breadcrumb["correlationId"])}")
            return exercise
        except Exception as e:
            logger.warning(f"A get_exercise Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_exercise", 
        function=get_exercise,
        description="Get a specific exercise", 
        arguments_schema={
            "description": "Exercise unique identifier (from get_exercises)",
            "type": "identifier",
        },
        output_schema={
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
                        
    logger.info("Registered exercise agent action handlers.")
    return agent
    