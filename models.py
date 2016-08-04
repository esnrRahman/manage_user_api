#!flask/bin/python

from app import db

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % self.name

class Group(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.date_created


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)