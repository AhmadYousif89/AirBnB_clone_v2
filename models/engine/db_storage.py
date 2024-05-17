#!/usr/bin/python3
"""Module handling database storage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.user import User

classes = {
    "City": City,
    "State": State,
    "Amenity": Amenity,
    "Review": Review,
    "Place": Place,
    "User": User,
}

HBNB_ENV = os.getenv("HBNB_ENV", "dev")
USER = os.getenv("HBNB_MYSQL_USER", "hbnb_dev")
PWD = os.getenv("HBNB_MYSQL_PWD", "hbnb_dev_pwd")
HOST = os.getenv("HBNB_MYSQL_HOST", "localhost")
DB = os.getenv("HBNB_MYSQL_DB", "hbnb_dev_db")


class DBStorage:
    """
    Implements a database storage engine for the application, using SQLAlchemy.

    Provides methods for creating connections, managing sessions,
    and performing CRUD operations on model objects.

    Attributes:
        __engine : The underlying SQLAlchemy engine connected to the database.
        __session : The current active session for database interactions.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database connection and creates a new session.

        Drops all tables if the environment variable `HBNB_ENV` is "test"
        to ensure a clean slate for testing purposes.
        """
        conn = f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}'
        self.__engine = create_engine(conn, pool_pre_ping=True)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves all instances of a given model class from the database.

        Args:
            cls (class, optional): The model class to retrieve instances for.
                Defaults to None, in which case it returns all objects from
                all registered model classes.

        Returns:
            dict: keys are constructed as `{class_name}.{object_id}`
                  and values are the corresponding model objects.
        """
        if cls and self.__session is not None:
            objs = self.__session.query(cls).all()
        else:
            objs = [
                obj
                for cls in classes.values()
                if self.__session is not None
                for obj in self.__session.query(cls).all()
            ]

        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objs}

    def new(self, obj):
        """
        Adds a new model object to the current session for persistence.

        Args:
            obj (object): The model object to be added to the database.
        """
        if self.__session is not None:
            self.__session.add(obj)

    def save(self):
        """
        Commits the current session to the database, persisting any changes.
        """
        if self.__session is not None:
            self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes a model object from the database.

        Args:
            obj (object, optional): The model object to be deleted.
                Defaults to None, in which case no object is deleted.
        """
        if obj is None:
            return
        if self.__session is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all database tables associated with registered model classes,
        effectively resetting the database schema.

        This method is typically used for testing or initialization purposes.
        """
        Base.metadata.create_all(self.__engine)
        make_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(make_session)
        self.__session = Session

    def close(self):
        """
        Removes the current session and closes the database connection.
        """
        if self.__session is not None:
            self.__session.remove()
        if self.__engine is not None:
            self.__engine.dispose()
