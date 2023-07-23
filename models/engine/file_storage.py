#!/usr/bin/python3
"""Module documentation for the FileStorage class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Defines the class FileStorage"""
    __file_path = "file.json"  # name of the fie to save objects/instances
    __objects = {}  # dict to store instances

    def all(self):
        """Returns the dictionary of abstracted objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects with key <obj_class_name>.id"""
        obj_cls_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_cls_name, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path"""
        objdict = FileStorage.__objects
        o_dict = {}
        for obj in objdict.keys():
            o_dict[obj] = objdict[obj].to_dict()
        with open(FileStorage.__file_path, "w") as _file:
            json.dump(o_dict, _file)

    def reload(self):
        "Deserializes the json str representation to python objects"""
        try:
            with open(FileStorage.__file_path) as _file:
                o_dict = json.load(_file)
                for obj in o_dict.values():
                    class_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            return
