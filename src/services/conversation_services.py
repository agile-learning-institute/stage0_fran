import datetime
from bson import ObjectId
from config.config import Config
import logging

from src.mongo_utils.mongo_io import MongoIO
logger = logging.getLogger(__name__)

class ConversationServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        return # No RBAC yet

    @staticmethod
    def get_conversations(token=None):
        """
        Get a list of the latest segment of all active conversations

        Args:
            token (token): Access Token from the requesting agent

        Returns:
            list: List of currently active conversations. (_id, name)
        """
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"$and": [
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        project = {"_id":1, "name":1}
        conversations = mongo.get_documents(config.CONVERSATION_COLLECTION_NAME, match, project)
        return conversations

    @staticmethod
    def get_all_conversations_by_name(query=None, token=None):
        """
        Get a list of conversation _id and name (channel_id)

        Args:
            query (str): Regex of channel_id values to return
            token (token): Access Token from the requesting agent

        Returns:
            list: List of { _id: "XX", name: "XX"} values
                where name matches the regex provided in the query parameter
                including inactive and archived documents   
        """
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"name": {"$regex": query}} if query else None
        project = {"_id":1, "name":1}
        conversations = mongo.get_documents(config.CONVERSATION_COLLECTION_NAME, match, project)
        return conversations

    @staticmethod
    def get_conversation(channel_id=None, token=None, breadcrumb=None):
        """Get the specified conversation"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"name": channel_id}
        conversations = mongo.get_documents(collection_name=config.CONVERSATION_COLLECTION_NAME, match=match)
        if len(conversations) == 0:
            return ConversationServices.add_conversation(data=match, token=token, breadcrumb=breadcrumb)
        return conversations[0]
    
    @staticmethod
    def add_conversation(data=None, token=None, breadcrumb=None):
        """Create a new conversation"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        data["status"] = config.ACTIVE_STATUS
        data["version"] = config.LATEST_VERSION
        data["last_saved"] = breadcrumb
        data["conversation"] = []
        mongo.create_document(collection_name=config.CONVERSATION_COLLECTION_NAME, document=data)
        return ConversationServices.get_conversation(channel_id=data["name"], token=token, breadcrumb=breadcrumb)
    
    @staticmethod
    def update_conversation(channel_id=None, data=None, token=None, breadcrumb=None):
        """Update the latest version of the specified conversation"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"$and": [
            {"name": channel_id},
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        data["last_saved"] = breadcrumb
        conversation = mongo.update_document(config.CONVERSATION_COLLECTION_NAME, match=match, set_data=data)
        return conversation
    
    @staticmethod
    def add_message(channel_id=None, message=None, token=None, breadcrumb=None):
        """Add a message to the conversation and generate a reply"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        
        # Fetch the existing conversation, create it if needed
        conversation = ConversationServices.get_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
        if len(conversation["conversation"]) > 1000: #TODO: Add config.MAX_MESSAGES
            pass # TODO - Add document_full or conversation_old roll-off logic here
        
        match = {"$and": [
            {"name": channel_id},
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        set_data = {"last_saved": breadcrumb}
        push_data = {"conversation": message}
        reply = mongo.update_document(config.CONVERSATION_COLLECTION_NAME, match=match, set_data=set_data, push_data=push_data)
        return reply["conversation"]

