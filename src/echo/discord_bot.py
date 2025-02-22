import discord
import json
import logging
from echo.echo import Echo
from echo.llm_handler import LLMHandler
from config import config

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class DiscordBot(discord.Client):
    def __init__(self, bot_framework, llm_handler, **kwargs):
        """
        Initializes the Discord bot with Echo framework and LLM handler.
        """
        intents = kwargs.pop("intents", discord.Intents.default())
        intents.messages = True
        intents.guilds = True
        intents.dm_messages = True  

        super().__init__(intents=intents, **kwargs)
        self.echo = bot_framework
        self.llm = llm_handler
        self.active_channels = []  

    async def on_ready(self):
        """Triggered when the bot successfully connects."""
        logger.info(f"Logged in as {self.user}")
        try:
            self.active_channels = self.echo.handle_command(f"/bot/get_channels/{json.dumps(config.DISCORD_BOT_NAME)}")
            logger.info(f"Initialized active channels: {self.active_channels}")
        except Exception as e:
            logger.warning(f"Failed to initialize active channels: {e}")

    async def on_message(self, message):
        """Processes incoming messages from Discord."""
        print(f"Got a message!")
        if message.author == self.user:
            return  # Ignore self-messages

        user_id = message.author.id
        username = message.author.username
        channel = message.channel.id if message.guild else f"DM-{user_id}"
        content = message.content
        response = None
        print(f"Processing message for user_id: {user_id}: channel: {channel} content: {content}")

        try:
            # Always Join DM channels if they are not already active
            if message.guild is None and channel not in self.active_channels:
                print(f"Joining DM Channel {channel}")
                response = self.update_active_channels("add_channel", channel)
                await message.channel.send(response)                
                
            # Leave Channels when requested
            if self.user in message.mentions and "leave" in content.lower():
                print(f"Leaving Channel {channel}")
                response = self.update_active_channels("remove_channel", channel)
                
            # Process Message if from an active channel            
            elif channel in self.active_channels:
                print(f"Getting LLM Response in {channel}")
                response = self.llm.handle_message(username, channel, content)
                
            # Join Channels when requested
            elif self.user in message.mentions and "join" in content.lower():
                print(f"Joining Channel {channel}")
                response = self.update_active_channels("add_channel", channel)

            # Send the reply message
            print(f"Sending response {response}")
            if response: await message.channel.send(response)
            return

        except Exception as e:
            logger.warning(f"Echo bot On-Message Error: {e}, user_id: {user_id}: channel: {channel} content: {content}")
            raise e

    def update_active_channels(self, action, channel):
        """
        Updates the list of active channels using the bot_agent actions.
        """
        try:
            self.active_channels = self.echo.handle_command(f"/bot/{action}/{json.dumps(channel)}")
            logger.info(f"Updated active channels list: {self.active_channels}")
            return f"✅ Channel: {channel} {'added to' if action == 'add_channel' else 'removed from'} active channels list."
        except Exception as e:
            raise Exception(f"Failed to update active channels: {e}")
