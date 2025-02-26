import discord
import json
import logging
logger = logging.getLogger(__name__)

class DiscordBot(discord.Client):
    """_summary_
        This class handles interactions with Discord, and implements the on_message
        event handler. It maintains the list of active channels that the bot is participating in 
        and implements the channel join/leave logic. It uses the LLM handle_message_function 
        to process any messages that are not join/leave messages.
    """
    def __init__(self, handle_command_function=None, handle_message_function=None,  bot_id=None, **kwargs):
        """
        Initializes the Discord bot 

        :param handle_command_function: Function used to execute an agent action.
        :param handle_message_function: Function used to ask the LLM to handle a message
        :param bot_id: Unique Identifier of the Bot Record in the stage0 system.
        """
        intents = kwargs.pop("intents", discord.Intents.default())
        intents.messages = True
        intents.guilds = True
        intents.dm_messages = True  

        super().__init__(intents=intents, **kwargs)
        self.handle_command = handle_command_function
        self.handle_message = handle_message_function
        self.bot_id = bot_id
        self.active_channels = []  

    async def on_ready(self):
        """
            Triggered when the bot successfully connects, trigger the loading of 
            active channels from the /bot/get_channels action
        """
        logger.info(f"Logged in as {self.user}")
        try:
            arguments = json.dumps(self.bot_id, separators=(',', ':'))
            self.active_channels = self.handle_command(f"/bot/get_channels/{arguments}")
            logger.info(f"Initialized active channels: {self.active_channels}")
        except Exception as e:
            logger.warning(f"Failed to initialize active channels: {e}")

    async def on_message(self, message):
        """
            Processes incoming messages from Discord. 
            Handles all join/leave logic
            Passes messages to the LLM handle_message_function
        """
        logger.debug(f"Got a message!")
        if message.author == self.user:
            return  # Ignore self-messages

        user_id = message.author.id
        username = message.author.username
        channel = message.channel.id if message.guild else f"DM-{user_id}"
        content = message.content
        response = None
        logger.debug(f"Processing message for user_id: {user_id}: channel: {channel} content: {content}")

        try:
            # Always Join DM channels if they are not already active
            if message.guild is None and channel not in self.active_channels:
                logger.debug(f"Joining DM Channel {channel}")
                response = self.update_active_channels("add_channel", channel)
                await message.channel.send(response)                
                
            # Leave Channels when requested
            if self.user in message.mentions and "leave" in content.lower():
                logger.debug(f"Leaving Channel {channel}")
                response = self.update_active_channels("remove_channel", channel)
                
            # Process Message if from an active channel            
            elif channel in self.active_channels:
                logger.debug(f"Getting LLM Response in {channel}")
                response = self.handle_message(username, channel, content)
                
            # Join Channels when requested
            elif self.user in message.mentions and "join" in content.lower():
                logger.debug(f"Joining Channel {channel}")
                response = self.update_active_channels("add_channel", channel)

            # Send the reply message
            if response: 
                logger.debug(f"Sending response {response}")
                await message.channel.send(response)
            return

        except Exception as e:
            logger.warning(f"Echo bot On-Message Error: {e}, user_id: {user_id}: channel: {channel} content: {content}")
            raise e

    def update_active_channels(self, action, channel):
        """
        Updates the list of active channels using the bot_agent actions.
        """
        try:
            arguments = json.dumps({"bot_id": self.bot_id,"channel_id": channel}, separators=(',', ':'))
            self.active_channels = self.handle_command(f"/bot/{action}/{arguments}")
            logger.debug(f"Updated active channels list: {self.active_channels}")
            return f"✅ Channel: {channel} {'added to' if action == 'add_channel' else 'removed from'} active channels list."
        except Exception as e:
            raise Exception(f"Failed to update active channels: {e}")
