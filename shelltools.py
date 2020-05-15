import asyncio
from app.libs.gino import init_db

loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())
