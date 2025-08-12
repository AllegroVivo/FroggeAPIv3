from typing import Any, Generator

from fastapi import HTTPException
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from .config import settings
################################################################################

engine = create_engine(
    settings.DEVELOPMENT_DATABASE_URL
    if settings.DEBUG
    else settings.PRODUCTION_DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
    pool_timeout=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

################################################################################
if engine.dialect.name == "sqlite":
    print("SQLite database detected, registering foreign key constraint listener.")

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

################################################################################
def get_db() -> Generator[Session, Any, None]:

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except DataError as e:
        db.rollback()
        print(f"DataError: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Input string too long for column: {str(e)}")
    except IntegrityError as e:
        db.rollback()
        print(f"IntegrityError: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Integrity error: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemyError: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        db.close()

################################################################################
