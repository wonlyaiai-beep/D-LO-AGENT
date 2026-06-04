import os
import redis
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_USER, CACHE_TTL


# Redis connection
r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def save_message(session_id, role, content):
    """Conversation history save karo"""
    key = f"dlo:chat:{session_id}"
    history = get_history(session_id)
    history.append({"role": role, "content": content})
    r.setex(key, CACHE_TTL, json.dumps(history))

def get_history(session_id):
    """Conversation history lo"""
    key = f"dlo:chat:{session_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return []

def save_lead(session_id, lead_data):
    """Lead info save karo"""
    key = f"dlo:lead:{session_id}"
    r.setex(key, 86400, json.dumps(lead_data))

def get_lead(session_id):
    """Lead info lo"""
    key = f"dlo:lead:{session_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return {}

def clear_session(session_id):
    """Session clear karo"""
    r.delete(f"dlo:chat:{session_id}")
    r.delete(f"dlo:lead:{session_id}")