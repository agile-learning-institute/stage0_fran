import unittest
from unittest.mock import patch, AsyncMock
from src.services.bot_services import BotServices

class TestBotServices(unittest.IsolatedAsyncioTestCase):

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_get_bots(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.get_documents.return_value = [{"_id": "bot1", "name": "Test Bot", "description": "Test Desc"}]

        token = {"user_id": "test_user"}
        result = await BotServices.get_bots("query", token)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Bot")

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_get_bot(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.get_document.return_value = {"_id": "bot1", "name": "Test Bot"}

        token = {"user_id": "test_user"}
        result = await BotServices.get_bot("bot1", token)
        self.assertEqual(result["_id"], "bot1")

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_update_bot(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.update_document.return_value = {"_id": "bot1", "last_saved": "breadcrumb"}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"name": "Updated Bot"}

        result = await BotServices.update_bot("bot1", token, breadcrumb, data)
        self.assertEqual(result["last_saved"], "breadcrumb")

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_get_channels(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.get_document.return_value = {"channels": ["channel1", "channel2"]}

        token = {"user_id": "test_user"}
        result = await BotServices.get_channels("bot1", token)
        self.assertIn("channel1", result)

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_add_channel(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.update_document.return_value = {"channels": ["channel1", "channel2"]}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        result = await BotServices.add_channel("bot1", token, breadcrumb, "channel2")
        self.assertIn("channel2", result)

    @patch('src.services.bot_services.MongoIO.get_instance')
    @patch('src.services.bot_services.Config.get_instance')
    async def test_remove_channel(self, mock_config, mock_mongo):
        mock_mongo_instance = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = AsyncMock()
        mock_mongo_instance.update_document.return_value = {"channels": ["channel1"]}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        result = await BotServices.remove_channel("bot1", token, breadcrumb, "channel2")
        self.assertNotIn("channel2", result)

if __name__ == '__main__':
    unittest.main()
