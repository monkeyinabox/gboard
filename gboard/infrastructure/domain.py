from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from gboard import db
''' from gboard.infrastructure.server import Server '''

import json
import datetime

from dns import query, zone

from gboard.constants import STRING_SIZE

domain_server = Table('association', db.Model.metadata,
    Column('domain_id', Integer, ForeignKey('domain.id'), primary_key=True),
    Column('server_id', Integer, ForeignKey('server.id'), primary_key=True)
)

class Domain(db.Model):
   
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True)
    name = Column(
        String(STRING_SIZE),
        nullable=False,
        unique=True
    )
    servers = relationship('Server', secondary=domain_server, lazy='subquery',
        backref=db.backref('domain', lazy=True))

    rrs = relationship('ResourceRecord', backref='domian', lazy=True)

'''     def axfr(self):
        print('gather Zone info...')
        z = dns.zone.from_xfr(dns.query.xfr(server, domain))
        names = z.nodes.keys()
        for a in names:
                [zl].append(str(a)+'.'+domain)
        return zl '''