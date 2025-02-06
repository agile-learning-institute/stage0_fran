import discord
import logging

logger = logging.getLogger(__name__)

class Bot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.event_handlers = {}

    def register_handler(self, event_name, handler):
        """ Register a new event handler """
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append(handler)
        logger.info(f"Registered handler {handler.__name__} for event '{event_name}'")

    async def on_event(self, event_name, *args, **kwargs):
        """ Dispatch event to all registered handlers """
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                await handler(*args, **kwargs)

    async def on_ready(self):
        await self.on_event("on_ready")

    async def on_message(self, message):
        await self.on_event("on_message", message)

    async def on_reaction_add(self, reaction, user):
        await self.on_event("on_reaction_add", reaction, user)