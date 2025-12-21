from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import oracledb
from sqlalchemy.pool import NullPool
from app.core.config import settings

if settings.DB_THICK_MODE:
    oracledb.init_oracle_client(lib_dir=settings.ORACLEDB_LIB_DIR)

pool = oracledb.create_pool_async(
    user=settings.DB_USER, 
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST, 
    port=settings.DB_PORT, 
    service_name=settings.DB_SERVICE_NAME,
    min=settings.DB_MIN_POOL, 
    max=settings.DB_MAX_POOL, 
    increment=settings.DB_INCREMENT_POOL
)

async def get_connection():
    return await pool.acquire()

engine = create_async_engine(
    "oracle+oracledb://", 
    async_creator=get_connection, 
    poolclass=NullPool
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    autoflush=False, 
    autocommit=False,
    expire_on_commit=False
)

Base = declarative_base()