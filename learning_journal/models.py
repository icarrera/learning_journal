from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Unicode,
    UnicodeText,
    )

from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True)
    text = Column(UnicodeText)
    created = Column(DateTime, onupdate=datetime.datetime.utcnow)

Index('entry_index', Entry.title, unique=True)
