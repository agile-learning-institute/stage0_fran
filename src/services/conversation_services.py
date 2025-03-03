from datetime import datetime
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
        project = {"_id":1, "channel_id":1}
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
        match = {"channel_id": {"$regex": query}} if query else None
        project = {"_id":1, "channel_id":1}
        conversations = mongo.get_documents(config.CONVERSATION_COLLECTION_NAME, match, project)
        return conversations

    @staticmethod
    def get_conversation(channel_id=None, token=None, breadcrumb=None):
        """Get the specified conversation"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"$and": [
            {"channel_id": channel_id},
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        conversations = mongo.get_documents(collection_name=config.CONVERSATION_COLLECTION_NAME, match=match)
        if len(conversations) == 0:
            data = {}
            data["channel_id"] = channel_id
            data["status"] = config.ACTIVE_STATUS
            data["version"] = config.LATEST_VERSION
            data["last_saved"] = breadcrumb
            data["messages"] = []
            new_id = mongo.create_document(collection_name=config.CONVERSATION_COLLECTION_NAME, document=data)
            conversation = mongo.get_document(collection_name=config.CONVERSATION_COLLECTION_NAME, document_id=new_id)
            return conversation
        else:
            return conversations[0]
        
    @staticmethod
    def update_conversation(channel_id=None, data=None, token=None, breadcrumb=None):
        """Update the latest version of the specified conversation"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"$and": [
            {"channel_id": channel_id},
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
        if len(conversation["messages"]) > 1000: #TODO: Add config.MAX_MESSAGES
            conversation = ConversationServices.reset_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
        
        match = {"$and": [
            {"channel_id": channel_id},
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        set_data = {"last_saved": breadcrumb}
        push_data = {"messages": message}
        reply = mongo.update_document(config.CONVERSATION_COLLECTION_NAME, match=match, set_data=set_data, push_data=push_data)
        messages = reply["messages"]
        logger.debug(f"add_message update_document last message in reply: {messages[len(messages)-1]}")
        return messages

    @staticmethod
    def reset_conversation(channel_id=None, token=None, breadcrumb=None):
        """Move the active conversation to full and set the version string"""
        ConversationServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        
        match = {"$and": [
            {"channel_id": channel_id},
            {"version": config.LATEST_VERSION},
            {"status": config.ACTIVE_STATUS}
        ]}
        set_data = {
            "version": datetime.now().strftime("%Y-%m-%d%H:%M:%S"),
            "status": config.COMPLETED_STATUS,
            "last_saved": breadcrumb
        }
        reply = mongo.update_document(config.CONVERSATION_COLLECTION_NAME, match=match, set_data=set_data)
        if reply:
            messages = reply["messages"]
            last_message = messages[len(messages)-1]
            logger.debug(f"reset_conversation update_document, last message in reply: {last_message}")
            return reply
        else:
            logger.debug(f"reset_conversation no document to update")
            return {}

