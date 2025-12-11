from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        # Set timeout to 5s so Vercel doesn't kill the function (default 10s limit)
        self.client = AsyncIOMotorClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)

    def close(self):
        if self.client:
            self.client.close()

    def get_db(self):
        return self.client["wedding_app"]

    def get_dynamic_collection(self, collection_name: str):
        return self.client["wedding_app"][collection_name]

db = Database()
