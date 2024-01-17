#!/usr/bin/python3
"""
This module defines class DBStorage for project
"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Represents database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize new DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER", "root")
        password = getenv("HBNB_MYSQL_PWD", "")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        database = getenv("HBNB_MYSQL_DB", "hbnb_dev")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".
            format(user, password, host, database),
            pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Access all objects belonging to the given class in the current database session.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in format <class name>.<obj id> = obj.
        """
        classes = [State, City, User, Place, Review, Amenity]

        if cls is None:
            objs = []
            for model_class in classes:
                objs.extend(self.__session.query(model_class).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls)

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add obj to current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Start a new session by creating all the tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close working SQLAlchemy session."""
        self.__session.close()
