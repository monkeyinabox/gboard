from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.utils import IPAddressType
from . import db

from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import FormField

from ..constants import STRING_SIZE

from domain import domain_server, DomainForm


class Server(db.Model):
   
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)

    ip_address = Column(
        IPAddressType(),
        nullable=False
    )

    fqdn = Column(
        String(STRING_SIZE),
        nullable=False
    )

    roles = [None]

    domains = relationship('Domain', secondary=domain_server, lazy='subquery',
        backref=db.backref('server', lazy=True))

class ServerForm(ModelForm):
    class Meta:
        model = Server
    
    domains = ModelFieldList(FormField(DomainForm))