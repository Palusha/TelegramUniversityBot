import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '')

DB_URI = os.getenv('DB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', '')
