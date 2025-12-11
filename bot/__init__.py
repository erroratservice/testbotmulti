import logging
import os
from pyrogram import Client
from .config import Config

# Create sessions dir
if not os.path.exists(Config.WORKDIR):
    os.makedirs(Config.WORKDIR)

# Setup Logging
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
LOGGER = logging.getLogger(__name__)

# Initialize MAIN BOT
bot = Client(
    "MainController",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir=Config.WORKDIR
)
