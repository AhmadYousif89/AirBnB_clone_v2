#!/usr/bin/python3
""" City Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        state = relationship('State', back_populates='cities')
        places = relationship(
            'Place', back_populates='cities', cascade='all, delete'
        )
    else:
        state_id = ""
        name = ""
