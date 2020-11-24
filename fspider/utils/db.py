import databases
from databases import Database

db: Database = None


async def create_db(settings: dict) -> "Database":
    global db
    if db is None:
        db = databases.Database(settings['DATABASE_URL'])
        await db.connect()
    return db
