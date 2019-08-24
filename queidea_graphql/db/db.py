from sqlalchemy import create_engine
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.ext.declarative import declarative_base

db_uri = 'postgresql+pg8000://postgres:postgres@localhost:5432/queidea'

engine = create_engine(db_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

# We will need this for querying
Base.query = db_session.query_property()
