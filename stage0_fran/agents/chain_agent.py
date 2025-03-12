import logging
from stage0_py_utils import Agent, create_echo_breadcrumb, create_echo_token
from stage0_fran.services.chain_services import ChainServices

logger = logging.getLogger(__name__)

def create_chain_agent(agent_name):
    """ Registers event handlers and commands for the Fran home channel. """
    agent = Agent(agent_name)
    
    def get_chains(arguments):
        """Get the list of Chain Names and IDs"""
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            chain = ChainServices.get_chains(token=token)
            logger.info(f"get_chains Successful {breadcrumb}")
            return chain
        except Exception as e:
            logger.warning(f"A get_chains Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name = "get_chains", 
        function = get_chains,
        description = "Get a list of chains", 
        arguments_schema = {"None"},
        output_schema = {
            "title": "Chains",
            "description": "Stage0 Exercise Chains",
            "type": "object",
            "properties": {
                "_id": {
                    "description": "The unique identifier for a Chain",
                    "type": "identifier"
                },
                "name": {
                    "description": "Chain Short Name",
                    "type": "word"
                }
            }
        })

    def get_chain(arguments):
        """Get a specific exercise chain"""
        try:
            token = create_echo_token()
            breadcrumb = create_echo_breadcrumb(token)
            chain = ChainServices.get_chain(chain_id=arguments, token=token)
            logger.info(f"get_chain Successful {breadcrumb}")
            return chain
        except Exception as e:
            logger.warning(f"A get_chain Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name= "get_chain", 
        function = get_chain,
        description = "Get a exercise chain", 
        arguments_schema = {
            "description": "Chain Unique Identifier",
            "type": "identifier"
        },
        output_schema = {
            "title": "Chain",
            "description": "A Chain of Exercises - a Template for a Workshop",
            "type": "object",
            "properties": {
                "_id": {
                    "description": "The unique identifier for a Chain",
                    "type": "identifier"
                },
                "status": {
                    "description": "The status of the chain",
                    "type": "enum",
                    "enums": "default_status"
                },
                "name": {
                    "description": "Chain short name, like Kickoff or Retrospective",
                    "type": "word"
                },
                "exercises": {
                    "description": "List of Exercise IDs",
                    "type": "array",
                    "items": {
                        "type": "identifier"
                    }
                },
                "last_saved": {
                    "description": "Last Saved breadcrumb",
                    "type": "breadcrumb"
                }
            }
        })

    logger.info(f"Registered chain agent action handlers.")
    return agent