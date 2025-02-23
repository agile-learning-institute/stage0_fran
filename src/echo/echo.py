import json
import re
from echo.agent import Agent

class Echo:
    
    def __init__(self, name=None, bot_id=None):
        """Initialize Echo with a registry of agents."""
        self.name = name
        self.bot_id = bot_id
        self.agents = {}

    def register_agent(self, agent_name: str, agent: Agent):
        """Registers an agent with Echo."""
        if not isinstance(agent, Agent):
            raise ValueError("Only instances of Agent can be registered.")
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
