from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,  # 30 seconds
        "pool_recycle": 1800,  # 30 minutes
        "pool_pre_ping": True,
    }

    return init_tcp_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    pool = create_engine(
        URL.create(
            drivername="postgresql",
            username=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
        ),
        **db_config,
    )
    pool.dialect.description_encoding = None
    return pool


engine = init_connection_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
