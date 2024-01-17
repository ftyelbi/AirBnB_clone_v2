#!/usr/bin/python3
"""
Module for FileStorage class.
"""
import json
from models.base_model import BaseModel

class FileStorage:
    """
    FileStorage class for serializing and deserializing objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects, optionally filtered by class.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """
        Adds a new object to __objects dictionary.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to JSON and writes to file.
        """
        obj_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes JSON file to __objects.
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    cls_name, obj_id = key.split('.')
                    cls = BaseModel.__subclasses__()[0]  # Assumes BaseModel as the parent class
                    obj = cls(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects.pop(key, None)

# Add documentation for the class and methods
"""
FileStorage class for serializing and deserializing objects.

Attributes:
    __file_path (str): Path to the JSON file.
    __objects (dict): Dictionary to store serialized objects.

Methods:
    all(self, cls=None): Returns a dictionary of all objects, optionally filtered by class.
    new(self, obj): Adds a new object to __objects dictionary.
    save(self): Serializes __objects to JSON and writes to file.
    reload(self): Deserializes JSON file to __objects.
    delete(self, obj=None): Deletes obj from __objects if it exists.
"""

# Ensure the script is executable
if __name__ == "__main__":
    pass
