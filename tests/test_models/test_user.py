#!/usr/bin/python3
"""Unittests for the User Class"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittest for testing instances of User class"""

    def test_type_of_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_publicstr(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_ispublic_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_ispublic_and_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_ispublic_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_ispublic_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def test_two_users_different_created_at(self):
        us1 = User()
        sleep(0.08)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def two_users_different_updated_at(self):
        us1 = User()
        sleep(0.08)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_str_representation(self):
        dt = datetime.now()
        dt_repr = repr(dt)
        us = User()
        us.id = "456789"
        us.created_at = us.updated_at = dt
        us_str = us.__str__()
        self.assertIn("[User] (456789)", us_str)
        self.assertIn("'id': '456789'", us_str)
        self.assertIn("'created_at': " + dt_repr, us_str)
        self.assertIn("'updated_at': " + dt_repr, us_str)

    def test_unused_args(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        us = User(id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "456")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def test_instantiation_with_nne_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing the  save method of the class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_once_(self):
        us = User()
        sleep(0.08)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def test_two_saves(self):
        us = User()
        sleep(0.08)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.08)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def test_save_with_args(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_updating_file(self):
        us = User()
        us.save()
        us_id = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(us_id, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method in User Class"""
    def test_to_dict(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_containing_correct_keya(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def teat_to_dict_containing_added_attr(self):
        us = User()
        us.nick_name = "Shicky"
        us.fav_no = 44
        self.assertEqual("Shicky", us.nick_name)
        self.assertIn("fav_no", us.to_dict())

    def test_to_dict_datetime_attr_are_str(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def test_output_to_dict(self):
        dt = datetime.now()
        us = User()
        us.id = "456789"
        us.created_at = us.updated_at = dt
        t_dict = {
            'id': "456789",
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), t_dict)

    def test_contrast_to_dict_and__dict__(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dict_with_args(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
