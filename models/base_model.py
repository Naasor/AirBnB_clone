#!/usr/bin/python3
"""Defines base model class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel

        Args:
            *args: Unused
            **kwargs (dict): key pair attribute
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, t_format)
                else:
                    self.__dict__[key] = value
        else:
            from .__init__ import storage
            models.storage.new(self)

    def save(self):
        """current datetime is saved at updated_at"""
        self.updated_at = datetime.now()
        from .__init__ import storage
        models.storage.save()

    def to_dict(self):
        """Returns the dictionary of the BaseModel instance"""
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()
        return inst_dict

    def __str__(self):
        """Print string representation of BaseModel inst."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
