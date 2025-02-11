import sys
import signal
import discord
from flask import Flask
from src.discord_utils.bot import Bot
from src.mongo_utils import mongo_io
from src.flask_utils.ejson_encoder import MongoJSONEncoder
from prometheus_flask_exporter import PrometheusMetrics

# Initialize Config
from src.config.config import Config
config = Config.get_instance()

# Initialize Logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Database Connection, and load one-time data
mongo = mongo_io.MongoIO.get_instance()
mongo.configure(config.WORKSHOP_COLLECTION_NAME)

# Initialize Flask App
app = Flask(__name__)
app.json = MongoJSONEncoder(app)

# Apply Prometheus monitoring middleware
metrics = PrometheusMetrics(app, path='/api/health/')
metrics.info('app_info', 'Application info', version=config.BUILT_AT)

# Register flask routes
from src.routes.config_routes import create_config_routes
from src.routes.chain_routes import create_chain_routes
from src.routes.exercise_routes import create_exercise_routes
from src.routes.workshop_routes import create_workshop_routes

app.register_blueprint(create_config_routes(), url_prefix='/api/config')
app.register_blueprint(create_chain_routes(), url_prefix='/api/chain')
app.register_blueprint(create_exercise_routes(), url_prefix='/api/exercise')
app.register_blueprint(create_workshop_routes(), url_prefix='/api/workshop')

# Initialize Discord Bot
bot = Bot(__name__)

# Register Discord Event Handlers
from src.handlers.fran_handlers import create_fran_handlers
from src.services.workshop_services import WorkshopServices
activeWorkshops = WorkshopServices.getActiveWorkshops()
bot.register_handlers(create_fran_handlers(activeWorkshops))

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
    bot.run()
    app.run(host='0.0.0.0', port=config.FRAN_API_PORT)