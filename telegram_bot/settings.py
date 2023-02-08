import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

DB_NAME = os.getenv('DB_NAME', '')
DB_URI = os.getenv('DB_URI', 'mongodb://localhost:27017/')

SUPPORTED_TYPES = ('text',)
