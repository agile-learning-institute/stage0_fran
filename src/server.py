import sys
import signal

# Initialize Singletons
from src.config.config import Config
from src.mongo_utils.mongo_io import MongoIO
config = Config.get_instance()
mongo = MongoIO.get_instance()

# Initialize Logging
import logging
logging.basicConfig(level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Initialize Database Connection, and load one-time data

# Initialize Flask App
from flask import Flask
from flask_utils.ejson_encoder import MongoJSONEncoder
from prometheus_flask_exporter import PrometheusMetrics
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.BUILT_AT)

# Register flask routes
from routes.bot_routes import create_bot_routes
from routes.conversation_routes import create_conversation_routes
from routes.config_routes import create_config_routes
from routes.chain_routes import create_chain_routes
from routes.exercise_routes import create_exercise_routes
from routes.workshop_routes import create_workshop_routes

app.register_blueprint(create_bot_routes(), url_prefix='/api/bot')
app.register_blueprint(create_conversation_routes(), url_prefix='/api/conversation')
app.register_blueprint(create_config_routes(), url_prefix='/api/config')
app.register_blueprint(create_chain_routes(), url_prefix='/api/chain')
app.register_blueprint(create_exercise_routes(), url_prefix='/api/exercise')
app.register_blueprint(create_workshop_routes(), url_prefix='/api/workshop')

# Initialize Discord Bot
from echo.echo import Echo
bot = Echo(__name__, bot_id=config.FRAN_BOT_ID)

# Register Discord Agents (Defaults to move to Echo package)
from agents.bot_agent import create_bot_agent
from agents.config_agent import create_config_agent
from agents.conversation_agent import create_conversation_agent
bot.register_agent(create_bot_agent(bot), agent_prefix="bot")
bot.register_agent(create_config_agent(bot), agent_prefix="config")
bot.register_agent(create_conversation_agent(bot), agent_prefix="conversation")

# Register Discord Agents specific to Fran
from agents.chain_agent import create_chain_agent
from agents.exercise_agent import create_exercise_agent
from agents.workshop_agent import create_workshop_agent
bot.register_agent(create_chain_agent(bot), agent_prefix="chain")
bot.register_agent(create_exercise_agent(bot), agent_prefix="exercise")
bot.register_agent(create_workshop_agent(bot), agent_prefix="workshop")

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")
    mongo.disconnect()
    logger.info('MongoDB connection closed.')
    bot.close()
    logger.info('Discord Bot connection closed.')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Start the bot and Expose the app object for Gunicorn
if __name__ == "__main__":
    bot.run(config.DISCORD_FRAN_TOKEN)
    app.run(host='0.0.0.0', port=config.FRAN_API_PORT)