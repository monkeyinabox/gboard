from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from . import db

from . import infrastructure

from .constants import STRING_SIZE

class User(db.Model, UserMixin):
   
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    email = Column(
        String(STRING_SIZE), 
        unique=True, 
        nullable=False
    )
    password = Column(
        String(STRING_SIZE),
        nullable=False                              
    )
    username = Column(
        String(STRING_SIZE),
        nullable=False
    )
    admin = Column( 
        Boolean, 
        nullable=False, 
        default=False)

    is_active = Column(
        Boolean, 
        nullable=False, 
        default=True
    )

    def __repr__(self):
        return '<User %r>' % self.email

    def email_exists(self):
        if db.session.query(User.id).filter_by(email=self.email).scalar() is not None:
            return False
        else:
            return True

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(
            User.username == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

    def get_name(self):
        return str(self.username)