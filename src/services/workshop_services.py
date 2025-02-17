from datetime import datetime
from config.config import Config
from mongo_utils.mongo_io import MongoIO
from services.chain_services import ChainServices
import discord

import logging

from src.services.conversation_services import ConversationServices
logger = logging.getLogger(__name__)

class WorkshopServices:

    @staticmethod 
    def _check_user_access(token):
        """Role Based Access Control logic"""
        return # No RBAC implemented yet

    @staticmethod
    async def get_workshops(query, token):
        """Get a list of workshops that have name that matches the provided query"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        match = {"name": {"$regex": query}} if query else None
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
    async def add_workshop(chain_id, data, token, breadcrumb):
        """Create a new workshop based on the provided chain of exercise and workshop data"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        chain = ChainServices.get_chain(chain_id, token)
        
        def _create_exercise(exercise_id):
            """Create a single exercises based on the exercise ID"""
            new_conversation_data = {
                "status": config.ACTIVE_STATUS,
                "version": config.LATEST_VERSION,
                "conversation": [],
                "last_saved": breadcrumb
            }
            new_conversation = ConversationServices.add_conversation(new_conversation_data, token, breadcrumb)
            new_exercise = {
                "exercise_id": exercise_id,
                "conversation_id": new_conversation["_id"],
                "status": config.PENDING_STATUS,
                "observations": []
            }
            return new_exercise
            
        # Build the list of exercises
        exercises = []
        for exercise_id in chain: 
            exercises.append(_create_exercise(exercise_id))

        # Build the new Workshop document        
        data["status"] = config.PENDING_STATUS
        data["current_exercise"] = 0
        data["exercises"] = exercises
        data["last_saved"] = breadcrumb

        workshop_id = await mongo.create_document(config.WORKSHOP_COLLECTION_NAME, data)
        workshop = await WorkshopServices.get_workshop(workshop_id, token)
        return workshop
    
    @staticmethod
    async def update_workshop(workshop_id, data, token, breadcrumb):
        """Update the specified workshop"""        
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        data["last_saved"] = breadcrumb
        workshop = await mongo.update_document(config.WORKSHOP_COLLECTION_NAME, workshop_id, data)
        return workshop

    @staticmethod
    async def start_workshop(workshop_id, token, breadcrumb):
        """Update the specified workshop Status to Active, record start time"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        data = {
            "status": config.ACTIVE_STATUS,
            "when": {
                "from": datetime.now()
            }
        }
        return await WorkshopServices.update_workshop(workshop_id, data, token, breadcrumb)
    
    @staticmethod
    async def add_observation(workshop_id, token, breadcrumb, observation):
        """Add an observation to the observations list"""
        WorkshopServices._check_user_access(token)
        config = Config.get_instance()
        mongo = MongoIO.get_instance()
        set_data = {"last_saved": breadcrumb}
        push_data = {"observations": observation}        
        await mongo.update_document(config.WORKSHOP_COLLECTION_NAME, workshop_id, set_data=set_data, push_data=push_data)
        return
