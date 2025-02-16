from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from config.config import Config
from mongo_utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):
        self.config = Config.get_instance()
        self.test_id = "eeee00000000000000009999"
        self.test_collection_name = "bots"
        
        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        mongo_io.configure(self.test_collection_name)

    def tearDown(self):
        mongo_io = MongoIO.get_instance()
        mongo_io.delete_document(self.test_collection_name, self.test_id)
        mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")

    def test_config_loaded(self):
        # Test that Config loaded version and enumerators
        self.assertIsInstance(self.config.versions, list)
        self.assertEqual(len(self.config.versions), 0)

        self.assertIsInstance(self.config.enumerators, dict)

    def test_CRUD_document(self):
        # Create a Test Document
        test_data = {
            "status": "Active",
            "name": "Test",
            "description": "A Test Bot",
            "channels": [],
            "last_saved": {
                  "fromIp": "",
                  "byUser": "",
                  "atTime": datetime(2025, 1, 1, 12, 34, 56),
                  "correlationId": ""
                } 
        }
        mongo_io = MongoIO.get_instance()
        self.test_id = mongo_io.create_document(self.test_collection_name, test_data)
        id_str = str(self.test_id)
        
        self.assertEqual(id_str, str(self.test_id))

        # Retrieve the document
        document = mongo_io.get_document(self.test_collection_name, id_str)
        self.assertIsInstance(document, dict)
        self.assertEqual(document, test_data)
        
        # Update the document
        test_update = {
            "description": "A New test value"
        }
        document = mongo_io.update_document(self.test_collection_name, id_str, test_update)
        self.assertIsInstance(document, dict)
        self.assertEqual(document["description"], "A New test value")
        
        
    def test_order_by_ASCENDING(self):
        mongo_io = MongoIO.get_instance()
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', ASCENDING)]        
        
        result = mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[1]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[3]["collectionName"], "exercises")
        self.assertEqual(result[4]["collectionName"], "workshops")

    def test_order_by_DESCENDING(self):
        mongo_io = MongoIO.get_instance()
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', DESCENDING)]        
        
        result = mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[4]["collectionName"], "bots")
        self.assertEqual(result[3]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[1]["collectionName"], "exercises")
        self.assertEqual(result[0]["collectionName"], "workshops")

    def test_get_all_full_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        result = mongo_io.get_documents(config.VERSION_COLLECTION_NAME)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")

    def test_get_some_full_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        match = {"collectionName":"chains"}
        result = mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "chains")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        
    def test_get_all_partial_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = mongo_io.get_documents(config.VERSION_COLLECTION_NAME, project=project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])
        
    def test_get_some_partial_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        match = {"collectionName":"conversations"}
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match, project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "conversations")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])

if __name__ == '__main__':
    unittest.main()