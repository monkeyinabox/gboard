# manage.py
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData, ForeignKeyConstraint, Table, DropConstraint, DropTable
from sqlalchemy.engine import reflection

from flask_script import Manager
#from flask.ext.migrate import Migrate, MigrateCommand

from gboard import app, db
from gboard.models import User

app.config.from_object('config')

manager = Manager(app)


@manager.command
def init():
    '''Initializes database'''
    db_DropEverything(db)
    db.create_all()
    create_admin()

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db_DropEverything(db)


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='gboard@genesis.swiss',
                        password='gboard',
                        username='gboard',
                        is_active=True))
    db.session.commit()

def db_DropEverything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()

if __name__ == '__main__':
    manager.run()
