import os
from dotenv import load_dotenv

load_dotenv()

# Bot
DEBUG = True if os.getenv('DEBUG', 'off') == 'on' else False
API_TOKEN = os.getenv('BOT_TOKEN')
