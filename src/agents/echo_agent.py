import logging
from echo_utils.breadcrumb import create_breadcrumb
from echo_utils.token import create_token
from config.config import Config
from echo.agent import Agent
from echo.echo import Echo

logger = logging.getLogger(__name__)

def create_echo_agent(agent_name, echo=None):
    """ Registers event handlers and commands for the Config Agent. """
    if not isinstance(echo, Echo):
        raise Exception("create_echo_agent Error: an instance of Echo is a required parameter")
    agent = Agent(agent_name)
    
    def get_agents(arguments):
        """ Slash command to get agent data"""
        try:
            token = create_token()
            breadcrumb = create_breadcrumb(token)
            agents = echo.get_agents()
            logger.info(f"get_agents Success {breadcrumb}")
            return agents
        except Exception as e:
            logger.warning(f"get_agents Error has occurred: {e}")
            return "error"
    agent.register_action(
        action_name="get_agents", 
        function=get_agents,
        description="Get the list of Agents and Actions", 
        arguments_schema="none",
        output_schema={
            "description": "List of agents",
            "type": "array",
            "items": {
                "description": "An echo agent instance",
                "type": "object"
            }
        }
    )

    logger.info("Registered echo agent action handlers.")
    return agent