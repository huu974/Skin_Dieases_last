"""
Redis缓存管理
"""
import redis
from app.core.config import settings
from typing import Optional, Any
import json


class RedisClient:
    def __init__(self):
        self.client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[str]:
        return self.client.get(key)
    
    def set(self, key: str, value: Any, expire: int = 3600):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        self.client.set(key, value, ex=expire)
    
    def delete(self, key: str):
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0
    
    def incr(self, key: str) -> int:
        return self.client.incr(key)
    
    def expire(self, key: str, seconds: int):
        self.client.expire(key, seconds)
    
    def hset(self, name: str, key: str, value: Any):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        self.client.hset(name, key, value)
    
    def hget(self, name: str, key: str) -> Optional[str]:
        return self.client.hget(name, key)
    
    def hgetall(self, name: str) -> dict:
        return self.client.hgetall(name)


redis_client = RedisClient()
