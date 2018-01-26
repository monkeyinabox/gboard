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

    ttl = Column(
        String(STRING_SIZE))

    rr_type = Column(
        String(STRING_SIZE))

    domain_id = Column(
        Integer,
        ForeignKey('domain.id'), 
        nullable=True)

    server_id = Column(
        Integer,
        ForeignKey('server.id'), 
        nullable=True)

    server = relationship('Server')

    def __init__(self, owner, data, ttl, rr_type, server_id):
        self.owner = owner
        self.data = data
        self.ttl = ttl
        self.rr_type = rr_type
        self.server_id = server_id