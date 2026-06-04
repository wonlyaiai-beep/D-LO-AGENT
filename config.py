import os
from dotenv import load_dotenv

load_dotenv()

# MODELS
PRIMARY_MODEL  = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

# API KEYS
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
EMAIL          = os.getenv("EMAIL")
EMAIL_PASS     = os.getenv("EMAIL_PASS")
NOTIFY_EMAIL   = os.getenv("NOTIFY_EMAIL")

# REDIS
REDIS_HOST     = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT     = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# SETTINGS
MAX_RETRIES    = 3
TIMEOUT        = 10
CACHE_TTL      = 3600