import discord
import logging

logger = logging.getLogger(__name__)

class Echo(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.event_handlers = {}

    def register_agent(self, create_agent):
        """ Register a new event handler """
        return

    async def on_event(self, message, *args, **kwargs):
        return

    async def on_ready(self):
        await self.on_event("on_ready")

    async def on_message(self, message):
        await self.on_event("on_message", message)

    async def on_reaction_add(self, reaction, user):
        await self.on_event("on_reaction_add", reaction, user)