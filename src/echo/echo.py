import json
import re
from echo.agent import Agent
from echo.discord_bot import DiscordBot
from echo.llm_handler import LLMHandler
from echo.ollama_llm_client import OllamaLLMClient


class Echo:
    """_summary_
    The Echo class is the container that coordinates
    action between the discord_bot and llm_handler. 
    Agents register their actions with Echo, and Echo
    implements the handle_command function used in
    those classes to execute agent/actions.
    """
    
    def __init__(self, name=None, bot_id=None):
        """Initialize Echo with a default agents."""
        self.name = name
        self.agents = {}        

        # Register default agents
        from agents.bot_agent import create_bot_agent
        from agents.conversation_agent import create_conversation_agent
        from agents.echo_agent import create_echo_agent
        self.register_agent(create_echo_agent(agent_name="echo", agents=self.agents))
        self.register_agent(create_bot_agent(agent_name="bot"))
        self.register_agent(create_conversation_agent(agent_name="conversation"))

        # Initialize LLM Conversation Handler
        self.llm_handler = LLMHandler(
            handle_command_function=self.handle_command, 
            llm_client=OllamaLLMClient()
        )
        # Initialize Discord Chatbot
        self.bot = DiscordBot(
            handle_command_function=self.handle_command, 
            handle_message_function=self.llm_handler.handle_message,
            bot_id=bot_id
        )
        
    def run(self, token):
        self.bot.run(token)
        
    def close(self):
        self.bot.close()

    def register_agent(self, agent, agent_name=None):
        """Registers an agent with Echo."""
        if not isinstance(agent, Agent): 
            raise Exception(f"can not register agent without actions: {agent}")
        self.agents[agent_name] = agent

    def get_agents(self):
        """Returns a list of registered agent names."""
        return list(self.agents.keys())

    def parse_command(self, command: str):
        """
        Parses a command in the format: /agent/action/arguments.
        Ensures only the first two slashes separate agent and action, 
        while keeping the arguments intact.
        """
        match = re.match(r"^/([^/]+)/([^/]+)/(.*)$", command)
        if not match:
            raise Exception(f"Invalid command format: {command}")

        agent_name, action_name, arguments_str = match.groups()

        # Parse JSON safely
        try:
            arguments = json.loads(arguments_str) if arguments_str else {}
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in arguments: {arguments_str}") from e

        return agent_name, action_name, arguments
    
    def handle_command(self, command: str):
        """
        Handles an incoming command.
        - Routes it to the correct agent and action.
        - Returns the response from the agent.
        - If invalid, returns an error message or silence (for unknown agents).
        """
        agent_name, action_name, arguments = self.parse_command(command)

        if agent_name not in self.agents:
            return ""  # Silence for unknown agents

        agent = self.agents[agent_name]

        if action_name not in agent.get_actions():
            available_actions = ", ".join(agent.get_actions())
            return f"Unknown action '{action_name}'. Available actions: {available_actions}"

        return agent.invoke_action(action_name, arguments)
