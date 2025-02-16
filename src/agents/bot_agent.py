import discord
import logging
from discord import app_commands
from services.bot_services import BotServices
from src.services.workshop_services import WorkshopServices

logger = logging.getLogger(__name__)

def create_bot_agent(bot):
    """ Registers event handlers and commands for the Fran home channel. """

    @bot.action(action_name="get_bot", 
                description="", 
                arguments_schema="",
                outputs_schema="")
    async def get_bot(arguments):
        """  """
        try
            await bot = BotServices.get_bot(arguments._id)
            return bot
        except Exception as e:
            logger.warning(f"Agent Get bot Error has occurred: {e}")
            return "error"
        
    logger.info("Registered Fran command handlers.")