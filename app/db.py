from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import Settings

engine = create_async_engine(Settings.DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from app.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
