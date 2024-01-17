#!/usr/bin/python3
"""the user class"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Represents user for MySQL database.

    Attributes:
        __tablename__: represents table name, users
        email: (sqlalchemy String): user's email address.
        password (sqlalchemy String): user's password.
        first_name (sqlalchemy String): user's first name.
        last_name (sqlalchemy String): user's last name.
        places (sqlalchemy relationship): user-Place relationship.
        reviews (sqlalchemy relationship): user-Review relationship.

    """

    __tablename__ = "users"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
