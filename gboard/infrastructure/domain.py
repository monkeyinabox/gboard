from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from gboard import db
from gboard.infrastructure.Server import Server
from gboard.infrastructure.ResourceRecord import ResourceRecord 
from sqlalchemy_utils import IPAddressType
from wtforms.validators import IPAddress


import json
import datetime
import dns
from dns import query, zone

from gboard.constants import STRING_SIZE

at_domain_server = Table('domain_server', db.Model.metadata,
    Column('server_id', Integer, ForeignKey('server.id'), primary_key=True),
    Column('domain_id', Integer, ForeignKey('domain.id'), primary_key=True)
)

class Domain(db.Model):
   
    __tablename__ = 'domain'
    id = Column(Integer, 
        primary_key=True)

    name = Column(
        String(STRING_SIZE),
        nullable=False,
        unique=True
    )
    master = Column(
            Integer, 
            ForeignKey('server.id'))

    server = relationship('Server', secondary=at_domain_server, lazy='subquery', 
            backref=db.backref('domains', lazy=True))

    rrs = relationship('ResourceRecord', backref='domain', lazy=True)

    @property
    def master_ip(self):
        return Server.query.get(self.master).ip_address.__str__()
    
    def axfr(self):
        zone = dns.zone.from_xfr(dns.query.xfr(self.master_ip, self.name))
        
        for rdtype in ['A', 'AAAA', 'NS', 'CNAME', 'SRV', 'TXT', 'SOA']:

            for (name, ttl, rdata) in zone.iterate_rdatas(rdtype=rdtype):
                rr = ResourceRecord(name.__str__(), rdata.__str__(), ttl.__str__(), rdtype, self.master)
                self.rrs.append(rr)

        db.session.commit()

        return True