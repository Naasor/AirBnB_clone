#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        key = "{}.{}".format(ocname, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        all_objs = FileStorage.__objects
        objdict = {}
        for obj in all_objs.keys():
            objdict[obj] = all_objs[obj].to_dict()
        with open(FileStorage.__file_path, "w", encoding='utf-8') as file:
            json.dump(objdict, file)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                try:
                    objdict = json.load(file)

                    for key, value in objdict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)

                        inst = cls(**value)

                        FileStorage.__objects[key] = inst
                except Exception:
                    pass
