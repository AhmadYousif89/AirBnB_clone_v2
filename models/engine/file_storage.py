#!/usr/bin/python3
"""Define the FileStorage class module"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review


classes = {
    'BaseModel': BaseModel,
    'Amenity': Amenity,
    'User': User,
    'City': City,
    'State': State,
    'Place': Place,
    'Review': Review,
}


class FileStorage:
    """
    Manage serialization and deserialization of class instances.

    Attributes:
    -   __file_path (str): The path to the Json file.
    -   __objects (dict): A dictionary containing every class instance.
    """

    __file_path = "hbnb.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns A dictionary containing all instances stored in __objects.
        """
        if cls is None:
            return self.__objects

        return {k: v for k, v in self.__objects.items() if v.__class__ == cls}

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id

        Args:
        -   obj (BaseModel): The object to be added.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w') as f:
            _dict = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(_dict, f)

    def delete(self, obj=None):
        """Deletes an object."""
        if obj is None:
            return

        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects:
            del self.__objects[key]
            self.save()

    def reload(self):
        """
        Deserializes the JSON file to objects
        (only if the JSON file (__file_path) exists; otherwise, do nothing)
        (If the file doesn't exist, no exception should be raised)
        """
        try:
            with open(self.__file_path) as f:
                result = f.read()
                if not result:
                    return
                _dict = json.loads(result)
                self.__objects = {
                    key: classes[key.split('.')[0]](**obj)
                    for key, obj in _dict.items()
                }
        except IOError:
            pass

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects
        """
        self.reload()
