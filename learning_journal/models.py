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
import psycopg2

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
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
    created = Column(DateTime, onupdate=datetime.datetime.utcnow)

    def _query():
        Session = DBSession
        query = Session.query(Entry).filter(Entry_title)
        query.all()
        conn = psycopg2.connect(dbname="learning_journal", user="")
        cur = conn.cursor()
        query = 'SELECT * FROM entries;'
        cur.execute(query)
        entry_list = cur.fetchall()
        return entry_list


Index('entry_index', Entry.title, unique=True)
