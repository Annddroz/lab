import os, hashlib
import redis

def get_client():
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=False)

def key_for(url: str) -> str:
    # קיצור דטרמיניסטי קצר (6 תווים)
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:6]

