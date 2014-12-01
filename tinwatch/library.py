from sqlalchemy import Column, Integer, String


class Library(Base):
    __tablename__ = 'library'

    id = Column(Integer, primary_key=True)
    path = Column(String)

    def __repr__(self):
        return self.path

