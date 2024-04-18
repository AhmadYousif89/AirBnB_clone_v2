#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place', secondary='place_amenity', back_populates='amenities'
        )
    else:
        name = ""
