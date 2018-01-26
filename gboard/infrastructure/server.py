from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy_utils import IPAddressType
from gboard import db

from wtforms.validators import IPAddress

from gboard.constants import STRING_SIZE
from gboard.infrastructure import Domain

class Server(db.Model):
   
    __tablename__ = 'server'

    id = Column(Integer, 
        primary_key=True)

    ip_address = Column(
        IPAddressType(),
        nullable=False,
        unique=True,
        info={'validators': IPAddress()}
    )

    fqdn = Column(
        String(STRING_SIZE),
        nullable=False,
        unique=True
    )

    roles = [None]

'''     domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship('Domain', backref='servers') '''