#!/usr/bin/env python

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from db import session

Base = declarative_base()
Base.query = session.query_property()

association_table = Table('association', Base.metadata,
                        Column('group_id', Integer, ForeignKey('groups.id')),
                        Column('user_id', Integer, ForeignKey('users.id')))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(64))
    email = Column(String(120))

    def __repr__(self):
        return '<User %r>' % self.name


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(64))
    date_created = Column(DateTime, default=datetime.utcnow)
    users = relationship("User", secondary=association_table)

    def __repr__(self):
        return '<Post %r>' % self.date_created


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)