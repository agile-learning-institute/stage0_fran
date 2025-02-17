import logging
import sys
from bson import ObjectId 
from pymongo import MongoClient
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: - Refactor to use connection pooling

class MongoIO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoIO, cls).__new__(cls, *args, **kwargs)
            cls._instance.connected = False
            cls._instance.client = None
            cls._instance.db = None
            cls._instance.config = Config.get_instance()
        return cls._instance

    def configure(self, enumerators_collection_key):
        """Initialize Config values for Versions and Enumerators"""
        self.config = Config.get_instance()

        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.config.MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=2000, socketTimeoutMS=5000)
            # TODO: Config timeout
            self.client.admin.command('ping')  # Force connection
            self.db = self.client.get_database(self.config.MONGO_DB_NAME)
            self.connected = True
            logger.info(f"Connected to MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to connect to MongoDB: {e} - exiting")
            sys.exit(1) # fail fast 

    def disconnect(self):
        """Disconnect from MongoDB."""
        if not self.connected: return
            
        try:
            if self.client:
                self.client.close()
                logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.fatal(f"Failed to disconnect from MongoDB: {e} - exiting")
            sys.exit(1) # fail fast 
      
    def get_documents(self, collection_name, match=None, project=None, sort_by=None):
        """
        Retrieve a list of documents based on a match, projection, and optional sorting.

        Args:
            collection_name (str): Name of the collection to query.
            match (dict, optional): MongoDB match filter. Defaults to {}.
            project (dict, optional): Fields to include or exclude. Defaults to None.
            sort_by (list of tuple, optional): Sorting criteria (e.g., [('field1', ASCENDING), ('field2', DESCENDING)]). Defaults to None.

        Returns:
            list: List of documents matching the query.
        """
        if not self.connected:
            return None

        # Default match and projection
        match = match or {}
        project = project or None
        sort_by = sort_by or None

        try:
            collection = self.db.get_collection(collection_name)
            cursor = collection.find(match, project)
            if sort_by: cursor = cursor.sort(sort_by)

            documents = list(cursor)
            return documents
        except Exception as e:
            logger.error(f"Failed to get documents from collection '{collection_name}': {e}")
            raise
                
    def update_document(self, collection_name, document_id, set_data=None, push_data=None, add_to_set_data=None, pull_data=None):
        """
        Update a document in the specified collection with optional set, push, add_to_set, and pull operations.

        Args:
            collection_name (str): Name of the collection to update.
            document_id (str): ID of the document to update.
            set_data (dict, optional): Fields to update or set. Defaults to None.
            push_data (dict, optional): Fields to push items into arrays. Defaults to None.
            add_to_set_data (dict, optional): Fields to add unique items to arrays. Defaults to None.
            pull_data (dict, optional): Fields to remove items from arrays. Defaults to None.

        Returns:
            dict: The updated document if successful, otherwise None.
        """
        if not self.connected:
            return None

        try:
            document_collection = self.db.get_collection(collection_name)
            document_object_id = ObjectId(document_id)

            match = {"_id": document_object_id}

            # Build the update pipeline
            pipeline = {}
            if set_data:
                pipeline["$set"] = set_data
            if push_data:
                pipeline["$push"] = push_data
            if add_to_set_data:
                pipeline["$addToSet"] = add_to_set_data
            if pull_data:
                pipeline["$pull"] = pull_data

            updated = document_collection.update_one(match, pipeline)

            if updated.matched_count == 0:
                raise Exception(f"Document Not Found {document_id}")

        except Exception as e:
            logger.error(f"Failed to update document: {e}")
            raise

        return self.get_document(collection_name, document_id)

    def get_document(self, collection_name, document_id):
        """Retrieve a document by ID."""
        if not self.connected: return None

        try:
            # Get the document
            collection = self.db.get_collection(collection_name)
            document_object_id = ObjectId(document_id)
            document = collection.find_one({"_id": document_object_id})
            return document
        except Exception as e:
            logger.error(f"Failed to get document: {e}")
            raise

    def create_document(self, collection_name, document):
        """Create a curriculum by ID."""
        if not self.connected: return None
        
        try:
            document_collection = self.db.get_collection(collection_name)
            result = document_collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create document: {e}")
            raise   

    def delete_document(self, collection_name, document_id):
        """Delete a document."""
        if not self.connected: return None

        try:
            document_collection = self.db[collection_name]
            document_object_id = ObjectId(document_id)
            result = document_collection.delete_one({"_id": document_object_id})
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise 
        
        return result.deleted_count
    
    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the MongoIO class."""
        if MongoIO._instance is None:
            MongoIO()
        return MongoIO._instance
