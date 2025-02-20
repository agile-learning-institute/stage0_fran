class Echo:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent, agent_prefix):
        self.agents[agent_prefix] = agent

    async def handle_command(self, agent_name, action, arguments, channel, message):
        """Executes an agent action if valid."""
        if agent_name not in self.agents:
            return f"Unknown agent: `{agent_name}`. Available: {', '.join(self.agents.keys())}"

        agent = self.agents[agent_name]
        if action not in agent.actions:
            return f"Unknown action `{action}`. Available: {', '.join(agent.get_actions())}"

        return await agent.actions[action](arguments, channel, message)