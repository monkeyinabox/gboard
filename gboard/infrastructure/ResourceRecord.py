from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy_utils import IPAddressType
from gboard import db

from gboard.constants import STRING_SIZE

class ResourceRecord(db.Model):
   
    __tablename__ = 'rr'

    id = Column(Integer, primary_key=True)

    owner = Column(
        String(STRING_SIZE))

    data = Column(
        String(STRING_SIZE))

    TTL = Column(
        Integer)

    rr_type = Column(
        String(STRING_SIZE))

    rr_raw = Column(
        String(STRING_SIZE))

    domain = Column(
        String(STRING_SIZE),
        ForeignKey('domain.name'), 
        nullable=True)