from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///tinsparrow.db', echo=True)

Base.metadata.create_all(engine)
