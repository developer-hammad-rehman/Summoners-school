from motor.motor_asyncio import AsyncIOMotorClient
from .env_config import MONGODB_URI


client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database("summoners-school")