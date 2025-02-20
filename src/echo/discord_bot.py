import discord
from echo import Echo
from LLM import LLMHandler

class DiscordBot(discord.Client):
    def __init__(self, bot_framework, llm_handler):
        super().__init__()
        self.echo = bot_framework
        self.llm = llm_handler

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        """Processes incoming messages from Discord."""
        if message.author == self.user:
            return  # Ignore self-messages

        response = await self.llm.handle_message(message)

        # Only send messages meant for the group
        if response.startswith("FROM: LLM\nTO: GROUP") or response.startswith("FROM: AGENT\nTO: GROUP"):
            formatted_response = response.replace("FROM: LLM\nTO: GROUP\nMESSAGE: ", "")
            formatted_response = formatted_response.replace("FROM: AGENT\nTO: GROUP\nMESSAGE: ", "")
            await message.channel.send(formatted_response)