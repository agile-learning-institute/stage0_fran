import sys
import signal
import threading
from werkzeug.serving import make_server

# Initialize Singletons
from config.config import Config
from mongo_utils.mongo_io import MongoIO
config = Config.get_instance()
mongo = MongoIO.get_instance()

# Initialize Logging
import logging
logging.basicConfig(level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Initialize Echo Discord Bot
from echo.echo import Echo
echo = Echo(__name__, bot_id=config.FRAN_BOT_ID)

# Register Config Agent
from agents.config_agent import create_config_agent
echo.register_agent(create_config_agent(agent_name="config"))

# Register Discord Agents
from agents.chain_agent import create_chain_agent
from agents.exercise_agent import create_exercise_agent
from agents.workshop_agent import create_workshop_agent
echo.register_agent(create_chain_agent(agent_name="chain"))
echo.register_agent(create_exercise_agent(agent_name="exercise"))
echo.register_agent(create_workshop_agent(agent_name="workshop"))

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

# Flask server management
server = make_server("0.0.0.0", config.FRAN_API_PORT, app)
flask_thread = threading.Thread(target=server.serve_forever)

# Define a signal handler for SIGTERM and SIGINT
def handle_exit(signum, frame):
    logger.info(f"Received signal {signum}. Initiating shutdown...")

    # Shutdown Flask gracefully
    if flask_thread.is_alive():
        logger.info("Stopping Flask server...")
        server.shutdown()
        flask_thread.join()

    # Disconnect from MongoDB
    mongo.disconnect()
    logger.info("MongoDB connection closed.")

    # Close the Discord bot
    echo.close()

    logger.info("Shutdown complete.")
    sys.exit(0)  

# Register the signal handler
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Start the bot and expose the app object for Gunicorn
if __name__ == "__main__":
    flask_thread.start()
    logger.info("Flask server started.")

    # Run Discord bot in the main thread
    echo.run(token=config.DISCORD_FRAN_TOKEN)
    