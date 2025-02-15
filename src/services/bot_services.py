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
    def get_bots(token):
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
    
bots = [
    {
        "name":"",
        "description":"",
        "introduction":"",
        "exercises": [
            
        ]    
    },
    {},
    {}
]    