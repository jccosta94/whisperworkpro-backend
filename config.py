import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres")

# API Configuration
API_TITLE = "WhisperWorkPro API"
API_DESCRIPTION = "WhatsApp-native service CRM backend"
API_VERSION = "1.0.0"

# CORS Configuration
ALLOWED_ORIGINS = ["*"]  # Configure for production

# Database Configuration
ECHO_SQL = False  # Set to True for debugging SQL queries

# Pagination defaults
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000

# Search configuration
MAX_SEARCH_RESULTS = 50