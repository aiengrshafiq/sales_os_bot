# db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# Create an asynchronous engine
engine = create_async_engine(settings.DATABASE_URL)

# Create a configured "AsyncSession" class
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency to get an async DB session."""
    async with AsyncSessionLocal() as session:
        yield session