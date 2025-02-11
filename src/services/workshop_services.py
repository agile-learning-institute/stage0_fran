from src.config.config import Config
from src.mongo_utils.mongo_io import MongoIO
from src.services.chain_services import ChainServices
import discord

import logging
logger = logging.getLogger(__name__)

class WorkshopServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        return # No RBAC implemented yet

    @staticmethod
    async def get_workshops(query, token):
        """Get a list of workshops that match query"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = None
        project = {"_id":1, "name": 1}
        workshops = await mongo.get_documents(config.EXERCISE_COLLECTION_NAME, match, project)
        return workshops

    @staticmethod
    async def get_workshop(workshop_id, token):
        """Get the specified workshop"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        workshop = await mongo.get_document(config.EXERCISE_COLLECTION_NAME, workshop_id)
        return workshop

    @staticmethod
    async def create_workshop(chain_id, users, token, breadcrumb):
        """Create a new workshop based on the chain"""    
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()

        # Build a workshop and create the mongo document
        chain = ChainServices.get_chain(chain_id, token)
        workshop = {
            "status": "scheduled",
            "users": users,
            "exercises": chain.exercises,
            "last_saved": breadcrumb,
        }
        workshop_id = await mongo.create_document(config.WORKSHOP_COLLECTION_NAME, workshop)
        workshop = await WorkshopServices.get_workshop(workshop_id, token)
        return workshop
    
    @staticmethod
    async def create_channel(workshop, guild, category):
        """Create a workshop Discord Channel"""    
        # Create a Discord channel for the workshop
        new_channel = await guild.create_text_channel(workshop._id, category=category)
        
        # Add users to the new channel
        for mention in workshop.users:
            user = discord.utils.get(guild.members, mention.strip())
            if user:
                await new_channel.set_permissions(user, read_messages=True, send_messages=True)
        return
    
    @staticmethod
    async def update_workshop(workshop_id, token, breadcrumb, data):
        """Update the specified workshop"""        
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        data.last_saved = breadcrumb
        workshop = await mongo.update_document(config.WORKSHOP_COLLECTION_NAME, workshop_id, data)
        return workshop
