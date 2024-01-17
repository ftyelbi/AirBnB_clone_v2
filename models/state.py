#!/usr/bin/python3
"""
Module for the State class.
"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """
    State class for storing state information.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if storage_type == "db":
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances with state_id
            equals to the current State.id.
            """
            return [city for city in storage.all("City").values() if city.state_id == self.id]
