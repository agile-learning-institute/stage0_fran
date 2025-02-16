from src.config.config import Config
import logging

from src.mongo_utils.mongo_io import MongoIO
logger = logging.getLogger(__name__)

class conversationServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        return # No RBAC yet

    @staticmethod
    def get_conversations(token):
        """Get a list of chains that match query"""
        conversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = None
        project = {"_id":1, "name":1}
        conversations = mongo.get_documents(config.conversation_COLLECTION_NAME, match, project)
        return conversations

    @staticmethod
    def get_conversation(channel_id, token):
        """Get the specified conversation"""
        conversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        conversation = mongo.get_document(config.conversation_COLLECTION_NAME, channel_id)
        return conversation
    
    @staticmethod
    def update_conversation(channel_id, token, breadcrumb, patch_data):
        """Update the specified conversation"""
        return
    
    @staticmethod
    def add_message(channel_id, token, breadcrumb, message):
        """Add a message to the conversation and generate a reply"""
        return

