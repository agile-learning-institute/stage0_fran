import signal
import sys
import discord
from src.discord_utils.bot import Bot

# Initialize Config
from src.config.config import Config
config = Config.get_instance()

# Initialize Logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Discord Bot
bot = Bot(__name__)

# Register Discord Event Handlers
from src.handlers.fran_handlers import create_fran_handlers
bot.register_handlers(create_fran_handlers(), channel=config.FRAN_CHANNEL_NAME)

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")
    bot.close()
    logger.info('Discord Bot connection closed.')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Start the bot
bot.run(config.DISCORD_TOKEN)
