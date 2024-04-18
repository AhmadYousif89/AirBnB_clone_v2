#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """State class"""

    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City', back_populates='state', cascade='all, delete'
        )
    else:
        name = ""

        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            from models.__init__ import storage
            from models.city import City

            return [
                city
                for city in storage.all(City).values()
                if city.state_id == self.id
            ]
