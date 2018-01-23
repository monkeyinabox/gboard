# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="lupon",
    version='0.3.3',
    url='https://www.lupon.ch',
    description='',
    author='Florian Rindlisbacher',
    author_email='florian.rindlisbacher@students.bfh.ch',
    packages=["lupon"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-Babel',
        #'Flask-Cache',
        'Flask-Mail',
        'Flask-WTF',
        'Flask-SQLAlchemy',
        'Flask-DebugToolbar',
         #'wtforms-sqlalchemy',
        'Flask-Login',
        'Flask-Bcrypt',
        'Flask-Script',
        'Psycopg2',
        'requests',
        'passlib',
        'requests',
        'Flask-Migrate'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
