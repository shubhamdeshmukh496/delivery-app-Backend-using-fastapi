from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import db_settings


engine = create_async_engine(db_settings.POSTGRES_url, echo=True)

Base = declarative_base()

AsyncSessionLocal =  sessionmaker(bind = engine, class_ = AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
