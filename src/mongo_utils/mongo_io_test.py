from copy import deepcopy
from datetime import datetime, timezone
import unittest

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from config.config import Config
from mongo_utils.mongo_io import MongoIO

class TestMongoIO(unittest.TestCase):
    
    async def setUp(self):
        self.config = Config.get_instance()
        self.test_id = "eeee00000000000000009999"
        self.test_collection_name = self.config.BOT_COLLECTION_NAME
        self.test_bot = {"status":"Active","name":"Test","description":"A Test Bot","channels":[],"last_saved":{"fromIp":"","byUser":"","atTime":datetime(2025, 1, 1, 12, 34, 56),"correlationId":""}}

        MongoIO._instance = None
        mongo_io = MongoIO.get_instance()
        await mongo_io.configure(self.test_collection_name)

    async def tearDown(self):
        mongo_io = MongoIO.get_instance()
        await mongo_io.delete_document(self.test_collection_name, self.test_id)
        await mongo_io.disconnect()
    
    async def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")

    async def test_config_loaded(self):
        # Test that Config loaded version and enumerators
        self.assertIsInstance(self.config.versions, list)
        self.assertEqual(len(self.config.versions), 0)

        self.assertIsInstance(self.config.enumerators, dict)

    async def test_CR_document(self):
        # Create a Test Document
        mongo_io = MongoIO.get_instance()
        self.test_id = await mongo_io.create_document(self.test_collection_name, self.test_bot)
        id_str = str(self.test_id)
        
        self.assertEqual(id_str, str(self.test_id))

        # Retrieve the document
        document = await mongo_io.get_document(self.test_collection_name, id_str)
        self.assertIsInstance(document, dict)
        self.assertEqual(document, self.test_bot)
        
    async def test_CRU_document(self):
        # Create a Test Document
        mongo_io = MongoIO.get_instance()
        self.test_id = await mongo_io.create_document(self.test_collection_name, self.test_bot)
        id_str = str(self.test_id)

        # Update the document with set data
        test_update = {"description": "A New test value"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, set_data=test_update)
        self.assertIsInstance(document, dict)
        self.assertEqual(document["description"], "A New test value")
        
    async def test_add_to_set_document(self):
        # Create a Test Document
        mongo_io = MongoIO.get_instance()
        self.test_id = await mongo_io.create_document(self.test_collection_name, self.test_bot)
        id_str = str(self.test_id)

        # Add a channel
        test_add_to_set = {"channels": "channel1"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Re-Add a channel (should no-op)
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Add another channel
        test_add_to_set = {"channels": "channel2"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 2)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel2")

    async def test_push_document(self):
        # Create a Test Document
        mongo_io = MongoIO.get_instance()
        self.test_id = await mongo_io.create_document(self.test_collection_name, self.test_bot)
        id_str = str(self.test_id)

        # Add a channel
        push_data = {"channels": "channel1"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, push_data=push_data)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Re-Add a channel (should add duplicate)
        document = await mongo_io.update_document(self.test_collection_name, id_str, push_data=push_data)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 2)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel1")

        # Add another channel
        test_add_to_set = {"channels": "channel2"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 3)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel1")
        self.assertEqual(document["channels"][2], "channel2")

    async def test_pull_from_document(self):
        # Create a Test Document
        mongo_io = MongoIO.get_instance()
        self.test_id = await mongo_io.create_document(self.test_collection_name, self.test_bot)
        id_str = str(self.test_id)

        # Add some channels
        test_add_to_set = {"channels": "channel1"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        test_add_to_set = {"channels": "channel2"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)

        # Remove channel1
        test_pull = {"channels": "channel1"}
        document = await mongo_io.update_document(self.test_collection_name, id_str, pull_data=test_pull)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel2")
        
    async def test_order_by_ASCENDING(self):
        mongo_io = MongoIO.get_instance()
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', ASCENDING)]        
        
        result = await mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[1]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[3]["collectionName"], "exercises")
        self.assertEqual(result[4]["collectionName"], "workshops")

    async def test_order_by_DESCENDING(self):
        mongo_io = MongoIO.get_instance()
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', DESCENDING)]        
        
        result = await mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[4]["collectionName"], "bots")
        self.assertEqual(result[3]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[1]["collectionName"], "exercises")
        self.assertEqual(result[0]["collectionName"], "workshops")

    async def test_get_all_full_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        result = await mongo_io.get_documents(config.VERSION_COLLECTION_NAME)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")

    async def test_get_some_full_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        match = {"collectionName":"chains"}
        result = await mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "chains")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        
    async def test_get_all_partial_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = await mongo_io.get_documents(config.VERSION_COLLECTION_NAME, project=project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])
        
    async def test_get_some_partial_documents(self):
        mongo_io = MongoIO.get_instance()
        config = Config.get_instance()
        match = {"collectionName":"conversations"}
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = await mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match, project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "conversations")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])

if __name__ == '__main__':
    unittest.main()