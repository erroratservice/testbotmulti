import motor.motor_asyncio
from bot.config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            _id=id,
            child_token=None,
            is_premium=False
        )

    async def add_user(self, id):
        user = await self.col.find_one({'_id': id})
        if not user:
            user = self.new_user(id)
            await self.col.insert_one(user)

    async def get_user_token(self, id):
        user = await self.col.find_one({'_id': id})
        return user.get('child_token', None) if user else None

    async def update_user_token(self, id, token):
        await self.add_user(id)
        await self.col.update_one(
            {'_id': id},
            {'$set': {'child_token': token}}
        )

db = Database(Config.MONGO_URI, Config.DB_NAME)
