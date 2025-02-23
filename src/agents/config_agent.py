import logging
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from config.config import Config

logger = logging.getLogger(__name__)

def create_config_agent(bot):
    """ Registers event handlers and commands for the Config Agent. """

    def get_config(arguments):
        """ Slash command to get config data"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            config = Config.get_instance()
            logger.info(f"get_config Success {breadcrumb}")
            return config.to_dict(token=token)
        except Exception as e:
            logger.warning(f"get_config Error has occurred: {e}")
            return "error"
    bot.register_action(
        action_name="get_config", 
        function=get_config,
        description="Get the Bot Configuration information", 
        arguments_schema="none",
        output_schema={
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

    logger.info("Registered config agent action handlers.")