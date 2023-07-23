#!/usr/bin/python3
""""Module documentantion for the BaseModel Class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """A class that defines base model"""

    def __init__(self, *args, **kwargs):
        """Initializes the Base Model"""
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            for m, n in kwargs.items():
                if m == "created_at" or m == "updated_at":
                    self.__dict__[m] = datetime.strptime(n, tformat)
                else:
                    self.__dict__[m] = n
        else:
            models.storage.new(self)

    def save(self):
        """Updates update_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """"Return the dictionary of the BaseModel instance"""
        newdict = self.__dict__.copy()
        newdict["created_at"] = self.created_at.isoformat()
        newdict["updated_at"] = self.updated_at.isoformat()
        newdict["__class__"] = self.__class__.__name__
        return newdict

    def __str__(self):
        """Returns the string of the BaseModel instance"""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
