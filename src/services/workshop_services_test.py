import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from src.services.workshop_services import WorkshopServices

class TestWorkshopServices(unittest.IsolatedAsyncioTestCase):

    @patch('src.services.workshop_services.MongoIO.get_instance')
    @patch('src.services.workshop_services.Config.get_instance')
    async def test_get_workshops(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.get_documents.return_value = [{"_id": "ws1", "name": "Workshop 1"}]

        token = {"user_id": "test_user"}
        result = await WorkshopServices.get_workshops("Workshop", token)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Workshop 1")

    @patch('src.services.workshop_services.MongoIO.get_instance')
    @patch('src.services.workshop_services.Config.get_instance')
    async def test_get_workshop(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.get_document.return_value = {"_id": "ws1", "name": "Workshop 1"}

        token = {"user_id": "test_user"}
        result = await WorkshopServices.get_workshop("ws1", token)
        self.assertEqual(result["_id"], "ws1")

    @patch('src.services.workshop_services.MongoIO.get_instance')
    @patch('src.services.workshop_services.ChainServices.get_chain')
    @patch('src.services.workshop_services.ConversationServices.add_conversation')
    @patch('src.services.workshop_services.Config.get_instance')
    async def test_add_workshop(self, mock_config, mock_add_conversation, mock_get_chain, mock_mongo):
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_get_chain.return_value = ["exercise1"]
        mock_add_conversation.return_value = {"_id": "conv1"}
        mock_mongo_instance.create_document.return_value = "ws1"
        mock_mongo_instance.get_document.return_value = {"_id": "ws1", "name": "New Workshop"}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"name": "New Workshop"}

        result = await WorkshopServices.add_workshop("chain1", data, token, breadcrumb)
        self.assertEqual(result["_id"], "ws1")

    @patch('src.services.workshop_services.MongoIO.get_instance')
    @patch('src.services.workshop_services.Config.get_instance')
    async def test_update_workshop(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.update_document.return_value = {"_id": "ws1", "updated": True}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"name": "Updated Workshop"}

        result = await WorkshopServices.update_workshop("ws1", data, token, breadcrumb)
        self.assertEqual(result["updated"], True)

    @patch('src.services.workshop_services.WorkshopServices.update_workshop')
    async def test_start_workshop(self, mock_update_workshop):
        mock_update_workshop.return_value = {"_id": "ws1", "status": "active"}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}

        result = await WorkshopServices.start_workshop("ws1", token, breadcrumb)
        self.assertEqual(result["status"], "active")

    @patch('src.services.workshop_services.MongoIO.get_instance')
    @patch('src.services.workshop_services.Config.get_instance')
    async def test_add_observation(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        observation = {"text": "New observation"}

        await WorkshopServices.add_observation("ws1", token, breadcrumb, observation)
        mock_mongo_instance.update_document.assert_awaited_once()

if __name__ == '__main__':
    unittest.main()
