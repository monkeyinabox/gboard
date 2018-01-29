from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy_utils import IPAddressType
from gboard import db

from wtforms.validators import IPAddress

from gboard.constants import STRING_SIZE
from gboard.infrastructure import Domain, ResourceRecord

import dns
from dns import query, zone
import datetime

class Snapshot(db.Model):
   
    __tablename__ = 'snapshot'

    id = Column(Integer, 
        primary_key=True)
    
    generated = Column(DateTime(timezone=False),
        default=datetime.datetime.utcnow)
 
    left_domain_id = Column(Integer, ForeignKey("domain.id"))
    right_domain_id = Column(Integer, ForeignKey("domain.id"))

    left_domain = relationship("Domain", foreign_keys=[left_domain_id])
    right_domain = relationship("Domain", primaryjoin='Snapshot.right_domain_id == Domain.id')

    result = []

    #def __init__(self):
        # self.left_domain.append(left_domain)
        #self.righ_domain.append(right_domain)

        # left_domain.axfr(self.id)
        # right_domain.axfr(self.id)
    
    @property
    def get_snapshot(self):
        return ResourceRecord.query.filter_by(snapshot_id=self.id).all()
        
    def compare(self, z1, z2):
        z1.axfr(self.id)
        z2.axfr(self.id)
        result = []

        for i in z1.rrs:
            print(i.__str__())
            if i in z2.rrs:
                self.result.append

        return result

    def zoneCompare(self, z1, z2):
        zoneDiff = []
        sourceZone = dns.zone.from_xfr(dns.query.xfr(z1.name, z1.master_ip))
        targetZone = dns.zone.from_xfr(dns.query.xfr(z2.name, z2.master_ip))

        for record in sourceZone.nodes.keys():
            print(record)
            if not record in targetZone.nodes.keys():
                zoneDiff.append(str(record))

        return zoneDiff