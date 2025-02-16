from src.config.config import Config
from src.mongo_utils.mongo_io import MongoIO

import logging
logger = logging.getLogger(__name__)

class BotServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""        
        return # No access control implemented yet

    @staticmethod
    def get_bots(query, token):
        """Get a list of bot names and ids"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {}
        project = {"_id":1, "name":1}
        bots = mongo.get_documents(config.CHAIN_COLLECTION_NAME, match, project)
        return bots

    @staticmethod
    def get_bot(bot_id, token):
        """Get the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        bot = mongo.get_document(config.CHAIN_COLLECTION_NAME, bot_id)
        return bot
    
    @staticmethod
    async def update_bot(bot_id, token, breadcrumb, data):
        """Update the specified workshop"""        
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        data.last_saved = breadcrumb
        workshop = await mongo.update_document(config.BOT_COLLECTION_NAME, bot_id, data)
        return workshop

    @staticmethod
    def get_channels(discord_token, token):
        """Get the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"discord_token": discord_token}
        bots = mongo.get_documents(config.BOT_COLLECTION_NAME, match)
        return bots[0]

    @staticmethod
    def add_channel(bot_id, token, breadcrumb, channel_id):
        """Add the channel to the specified bot"""

    @staticmethod
    def remove_channel(bot_id, token, breadcrumb, channel_id):
        """Get the specified bot"""
