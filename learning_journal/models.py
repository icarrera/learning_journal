from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Unicode,
    UnicodeText,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base
from pyramid.security import Allow, Everyone
from pyramid.security import ALL_PERMISSIONS
import datetime
import psycopg2

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    """Our Journal Entry class."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User", back_populates="entries")

@property
def __acl__(self):
    return [
        (Allow, Everyone, 'view'),
        (Allow, 'g:users', ALL_PERMISSIONS)
        (Allow, self.author.username, 'edit'),
    ]
