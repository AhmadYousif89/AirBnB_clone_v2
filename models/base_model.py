#!/usr/bin/python3
"""Module defining a base class for all models in the application."""

import os
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Base class for all models in the application.

    Attributes:
        id (uuid): Unique identifier for the model instance.
        created_at: Timestamp indicating when the instance was created.
        updated_at: Timestamp indicating when the instance was updated.
    """

    if HBNB_TYPE_STORAGE == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.now(), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a new BaseModel instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # from models import storage

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            del kwargs['__class__']
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            # storage.new(self)

    def __str__(self):
        """Returns a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates and saves the instance to storage."""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the BaseModel instance"""
        _dict = self.__dict__.copy()
        _dict["__class__"] = self.__class__.__name__
        _dict['created_at'] = _dict['created_at'].isoformat()
        _dict['updated_at'] = _dict['updated_at'].isoformat()
        if '_sa_instance_state' in _dict:
            del _dict['_sa_instance_state']
        return _dict

    def delete(self):
        """Deletes the instance from storage."""
        from models import storage

        storage.delete(self)
