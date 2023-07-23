#!/user/bin/python3
""" Unittests for the base_model module"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiating(unittest.TestCase):
    """Unittests for testing instantation of the BaseModel class"""

    def test_type_of_no_args_instantiation(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in__objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_if_id_is_publicstr(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_if_created_at_ispublicdatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_if_updated_at_ispublicdatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_2_instances_unique_id(self):
        Bm = BaseModel()
        Bmm = BaseModel()
        self.assertNotEqual(Bm.id, Bmm.id)

    def test_2_instances_different_created_at(self):
        bm = BaseModel()
        sleep(0.08)
        bmm = BaseModel()
        self.assertLess(bm.created_at, bmm.created_at)

    def test_2_instances_different_updated_at(self):
        bm = BaseModel()
        sleep(0.05)
        bmm = BaseModel()
        self.assertLess(bm.updated_at, bmm.updated_at)

    def test_str_representation(self):
        d_t = datetime.now()
        d_t_repr = repr(d_t)
        bm = BaseModel()
        bm.id = "456789"
        bm.created_at = bm.updated_at = d_t
        bm_str = bm.__str__()
        self.assertIn("[BaseModel] (456789)", bm_str)
        self.assertIn("'id': '456789'", bm_str)
        self.assertIn("'created_at': " + d_t_repr, bm_str)
        self.assertIn("'updated_at': " + d_t_repr, bm_str)

    def test_unused_arguments(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiating_with_kwargs(self):
        d_t = datetime.now()
        d_t_iso = d_t.isoformat()
        bm = BaseModel(id="456", created_at=d_t_iso, updated_at=d_t_iso)
        self.assertEqual(bm.id, "456")
        self.assertEqual(bm.created_at, d_t)
        self.assertEqual(bm.updated_at, d_t)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        bm = BaseModel("8", id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "456")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.created_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittest for testing the save method for the BaseModel class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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

    def test_one_save(self):
        bm = BaseModel()
        sleep(0.08)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_2_saves(self):
        bm = BaseModel()
        sleep(0.08)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.0)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_witharguments(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updating_file(self):
        bm = BaseModel()
        bm.save()
        bm_id = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bm_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittest for testing to_dict method of the BaseModel super class"""
    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_containing_right_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_containing_added_attributes(self):
        bm = BaseModel()
        bm.name = "shikanda"
        bm.fav_no = 44
        self.assertIn("name", bm.to_dict())
        self.assertIn("fav_no", bm.to_dict())

    def test_to_dict_datetime_attr_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        d_t = datetime.now()
        bm = BaseModel()
        bm.id = "456789"
        bm.created_at = bm.updated_at = d_t
        t_dict = {
            'id': '456789',
            '__class__': 'BaseModel',
            'created_at': d_t.isoformat(),
            'updated_at': d_t.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), t_dict)

    def test_contrast_to_dict_and__dict__(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_withargs(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)
            # the method should not accept any args, but you should call
            # it on an instance of a class


if __name__ == "__main__":
    unittest.main()
