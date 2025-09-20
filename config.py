"""
Configuration settings for WOWDrive Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Google Drive API configuration
GOOGLE_CREDENTIALS_FILE = 'client_secrets.json'
GOOGLE_TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
CHUNK_SIZE = 1024 * 1024  # 1MB chunks
PROGRESS_UPDATE_INTERVAL = 20  # seconds

# Rate limiting
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_PERIOD = 60  # seconds

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
