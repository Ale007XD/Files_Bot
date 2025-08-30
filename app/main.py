import asyncio
from app.db import init_db
from app.jobs import scheduler_loop

async def main():
    await init_db()
    await scheduler_loop()

if __name__ == "__main__":
    asyncio.run(main())
