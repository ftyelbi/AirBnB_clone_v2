#!/usr/bin/python3
"""
Module for the DBStorage class.
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel

class DBStorage:
    """
    DBStorage class for managing storage using SQLAlchemy and MySQL.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of DBStorage.
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB'),
                                              pool_pre_ping=True))

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects depending on the class name (argument cls).
        """
        objs = {}
        if cls:
            for obj in self.__session.query(cls).all():
                objs[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in ["User", "State", "City", "Amenity", "Place", "Review"]:
                for obj in self.__session.query(eval(cls)).all():
                    objs[obj.__class__.__name__ + '.' + obj.id] = obj
        return objs

    def new(self, obj):
        """
        Adds the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes from the current database session obj if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and reloads the current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
