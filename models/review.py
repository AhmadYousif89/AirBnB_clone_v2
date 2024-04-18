#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


class Review(BaseModel, Base):
    """Review class to store review information"""

    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        user = relationship('User', back_populates='reviews')
        place = relationship('Place', back_populates='reviews')
    else:
        place_id = ""
        user_id = ""
        text = ""
