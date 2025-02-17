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
    async def get_bots(query, token):
        """Get a list of bot names and ids"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = None
        project = {"_id":1, "name":1, "description": 1}
        bots = await mongo.get_documents(config.BOT_COLLECTION_NAME, match, project)
        return bots

    @staticmethod
    async def get_bot(bot_id, token):
        """Get the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        bot = await mongo.get_document(config.BOT_COLLECTION_NAME, bot_id)
        return bot
    
    @staticmethod
    async def update_bot(bot_id, token, breadcrumb, data):
        """Update the specified workshop"""        
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        data["last_saved"] = breadcrumb
        bot = await mongo.update_document(config.BOT_COLLECTION_NAME, bot_id, set_data=data)
        return bot

    @staticmethod
    async def get_channels(bot_id, token):
        """Get the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        bot = await mongo.get_document(config.BOT_COLLECTION_NAME, bot_id)
        return bot["channels"]

    @staticmethod
    async def add_channel(bot_id, token, breadcrumb, channel_id):
        """Add the channel to the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        set_data = { "last_saved": breadcrumb},
        add_to_set = { "channels": channel_id }

        bot = await mongo.update_document(config.BOT_COLLECTION_NAME, bot_id, set_data=set_data, add_to_set_data=add_to_set)
        return bot["channels"]

    @staticmethod
    async def remove_channel(bot_id, token, breadcrumb, channel_id):
        """Get the specified bot"""
        BotServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        set_data = { "last_saved": breadcrumb},
        pull_from_set = { "channels": channel_id }

        bot = await mongo.update_document(config.BOT_COLLECTION_NAME, bot_id, set_data=set_data, pull_data=pull_from_set)
        return bot["channels"]
