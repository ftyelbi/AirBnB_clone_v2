#!/usr/bin/python3
"""
Module for the BaseModel class.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage

Base = declarative_base()

class BaseModel:
    """
    BaseModel class for defining common attributes/methods for other classes.
    """

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def save(self):
        """
        Saves the current instance to the storage (models.storage).
        """
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.
        """
        obj_dict = dict(self.__dict__)
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict

    def delete(self):
        """
        Deletes the current instance from the storage (models.storage).
        """
        storage.delete(self)
