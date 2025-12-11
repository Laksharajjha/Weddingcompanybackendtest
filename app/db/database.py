from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URL)

    def close(self):
        if self.client:
            self.client.close()

    def get_db(self):
        return self.client["wedding_app"]

    def get_dynamic_collection(self, collection_name: str):
        return self.client["wedding_app"][collection_name]

db = Database()
