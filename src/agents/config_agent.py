import logging
from echo import Blueprint
from config.config import Config
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token

logger = logging.getLogger(__name__)

def create_config_agent(bot):
    """ Registers event handlers and commands for the Fran home channel. """
    config_agent = Blueprint('conversation_agent', __name__)

    @config_agent.action(action_name="get_config", 
        description="Get the Bot Configuration information", 
        arguments_schema={},
        outputs_schema={
            "type": "object",
            "description": "",
            "properties": {
                "config_items": {
                    "description": "List of Configuration Items and non-secret values",
                   "type": "array"
                },
                "versions": {
                    "description": "List of database collection versions",
                    "type": "array"
                },
                "enumerators": {
                    "description": "Collection of Enumerators",
                    "type": "object"
                },
                "token": {
                    "description": "Data extracted from the token used when requesting configuration data",
                    "type": "object"
                }
            }
        }
    )
    async def get_config(arguments):
        """ Slash command to get config data"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            config = Config.get_instance()
            logger.info(f"Get Exercise Success {breadcrumb}")
            return config
        except Exception as e:
            logger.warning(f"Get Exercise Action Error has occurred: {e}")
            return "A processing error occurred"
