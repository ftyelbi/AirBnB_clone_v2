#!/usr/bin/python3
"""place class"""
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity, place_amenity
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import models


class Place(BaseModel, Base):
    """Represents Place for MySQL database.

    Inherits from SQLAlchemy Base and links to MySQL table places.

    Attributes:
        __tablename__ (str): name of MySQL table to store places.
        city_id (sqlalchemy String): place's city id.
        user_id (sqlalchemy String): place's user id.
        name (sqlalchemy String): name.
        description (sqlalchemy String): description.
        number_rooms (sqlalchemy Integer): number of rooms.
        number_bathrooms (sqlalchemy Integer): number of bathrooms.
        max_guest (sqlalchemy Integer): maximum number of guests.
        price_by_night (sqlalchemy Integer): price by night.
        latitude (sqlalchemy Float): place's latitude.
        longitude (sqlalchemy Float): place's longitude.
        reviews (sqlalchemy relationship): user-Review relationship.
        amenities (sqlalchemy relationship): user-Amenity relationship.
        amenity_ids (list): id list of all linked amenities

    """

    __tablename__ = "places"

    if getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(128))
        number_rooms = Column(Integer, default=0)
        number_bathrooms = Column(Integer, default=0)
        max_guest = Column(Integer, default=0)
        price_by_night = Column(Integer, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship('Amenity', secondary=place_amenity,
                                 back_populates='place_amenities',
                                 viewonly=False)
        amenity_ids = []
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Gets list of all linked Reviews.
            """

            review_list = []

            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)

            return review_list

        @property
        def amenities(self):
            """the Get and Set linked Amenities.
            """

            amenity_list = []

            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)

            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """Adding Amenity.id to amenity_ids
            """

            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
