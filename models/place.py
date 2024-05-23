#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from models import storage_type


if storage_type == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False,
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False,
        ),
    )


class Place(BaseModel, Base):
    """A place to stay"""

    if storage_type == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        cities = relationship('City', back_populates='places')
        user = relationship('User', back_populates='places')
        reviews = relationship(
            'Review', back_populates='place', cascade='all, delete'
        )
        amenities = relationship(
            "Amenity", secondary='place_amenity', viewonly=False
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            from models.__init__ import storage

            return [
                review
                for review in storage.all(Review).values()
                if review.state_id == self.id
            ]

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            from models.__init__ import storage

            return [
                amenity
                for amenity in storage.all(Amenity).values()
                if amenity.state_id == self.id
            ]
