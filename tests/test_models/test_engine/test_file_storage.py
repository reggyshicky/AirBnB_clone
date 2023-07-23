#!/usr/bin/python3
"""Defines the Unittests for file_storage.py"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiating(unittest.TestCase):
    """Unittests on the instance creation of the FileStorage class"""

    def test_FileStorage_instantiation_with_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantion_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_Private_str_filepath(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))
        # _FileStorage is used as a name mangling mechanism to access the
        # the __file_path attr of the FileStorage class

    def test_FileStorage_Private_dict_objs(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initialization(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittest for testing the methods in the FileStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # the intention of renaming is to create a temporary backup of the
        # original "file.json" before running tests
        # if exception occurs and is caught and pass statement is executed,
        # it allows test to proceed without interruption even if renamimg
        # fails

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        Bm = BaseModel()
        Us = User()
        St = State()
        Pl = Place()
        Cy = City()
        Am = Amenity()
        Rv = Review()
        models.storage.new(Bm)
        models.storage.new(Us)
        models.storage.new(St)
        models.storage.new(Pl)
        models.storage.new(Cy)
        models.storage.new(Am)
        models.storage.new(Rv)
        self.assertIn("BaseModel." + Bm.id, models.storage.all().keys())
        self.assertIn(Bm, models.storage.all().values())
        self.assertIn("User." + Us.id, models.storage.all().keys())
        self.assertIn(Us, models.storage.all().values())
        self.assertIn("State." + St.id, models.storage.all().keys())
        self.assertIn(St, models.storage.all().values())
        self.assertIn("Place." + Pl.id, models.storage.all().keys())
        self.assertIn(Pl, models.storage.all().values())
        self.assertIn("City." + Cy.id, models.storage.all().keys())
        self.assertIn(Cy, models.storage.all().values())
        self.assertIn("Amenity." + Am.id, models.storage.all().keys())
        self.assertIn(Am, models.storage.all().values())
        self.assertIn("Review." + Rv.id, models.storage.all().keys())
        self.assertIn(Rv, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)
            # new method only accepts args which are instances of a class

    def test_new_with_NoneArg(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        Bm = BaseModel()
        Us = User()
        St = State()
        Pl = Place()
        Cy = City()
        Am = Amenity()
        Rv = Review()
        models.storage.new(Bm)
        models.storage.new(Us)
        models.storage.new(St)
        models.storage.new(Pl)
        models.storage.new(Cy)
        models.storage.new(Am)
        models.storage.new(Rv)
        models.storage.save()
        saved_txt = ""
        with open("file.json", "r") as f:
            saved_txt = f.read()
            self.assertIn("BaseModel." + Bm.id, saved_txt)
            self.assertIn("User." + Us.id, saved_txt)
            self.assertIn("State." + St.id, saved_txt)
            self.assertIn("Place." + Pl.id, saved_txt)
            self.assertIn("City." + Cy.id, saved_txt)
            self.assertIn("Amenity." + Am.id, saved_txt)
            self.assertIn("Review." + Rv.id, saved_txt)

    def test_save_withargs(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        Bm = BaseModel()
        Us = User()
        St = State()
        Pl = Place()
        Cy = City()
        Am = Amenity()
        Rv = Review()
        models.storage.new(Bm)
        models.storage.new(Us)
        models.storage.new(St)
        models.storage.new(Pl)
        models.storage.new(Cy)
        models.storage.new(Am)
        models.storage.new(Rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + Bm.id, objs)
        self.assertIn("User." + Us.id, objs)
        self.assertIn("State." + St.id, objs)
        self.assertIn("Place." + Pl.id, objs)
        self.assertIn("City." + Cy.id, objs)
        self.assertIn("Amenity." + Am.id, objs)
        self.assertIn("Review." + Rv.id, objs)

    def test_reload_withargs(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
