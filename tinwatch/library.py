from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///tinsparrow.db', echo=True)
Base = declarative_base()


class Library(Base):
    __tablename__ = 'library'

    id = Column(Integer, primary_key=True)
    path = Column(String)

    def __repr__(self):
        return self.path


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    filename = Column(String)
    fingerprint = Column(String)
    artist = Column(String)
    album = Column(String)
    title = Column(String)
    track = Column(Integer)
    length = Column(Float)
    uploaded = Column(Boolean, default=False)

    def __repr__(self):
        return self.filename


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
