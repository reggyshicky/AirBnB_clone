#!/usr/bin/python3
"""Defines the unittests for Subclass Amenity.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiating(unittest.TestCase):
    """Unittest for testing the instantiation of the class Amenity"""
    def test_type_no_args_instantiation(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_if_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_if_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_if_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_if_name_is_public_cls_attr(self):
        Am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", Am.__dict__)
        # __dict__ stores instance specific attributes, so the assertNotIn
        # ensures that "name" attr is not instance specific attr but a
        # class attr

    def test_2_amenity_instances_withunique_ids(self):
        Am = Amenity()
        Amm = Amenity()
        self.assertNotEqual(Am.id, Amm.id)

    def test_if_2_amenities_have_diff_created_at(self):
        Am = Amenity()
        sleep(0.08)
        Amm = Amenity()
        self.assertLess(Am.created_at, Amm.created_at)

    def test_str_representation(self):
        d_time = datetime.now()
        d_time_rep = repr(d_time)
        # repr returns a str rep of the object
        Am = Amenity()
        Am.id = "456789"
        Am.created_at = Am.updated_at = d_time
        Am_str = Am.__str__()
        self.assertIn("[Amenity] (456789)", Am_str)
        self.assertIn("'id': '456789'", Am_str)
        self.assertIn("'created_at': " + d_time_rep, Am_str)
        self.assertIn("'updated_at': " + d_time_rep, Am_str)

    def test_unused_arguments(self):
        Am = Amenity(None)
        self.assertNotIn(None, Am.__dict__.values())

    def test_instantation_with_kwargs(self):
        """instantantating with **kwarsgs test method"""
        d_t = datetime.now()
        d_t_iso = d_t.isoformat()
        Am = Amenity(id="678", created_at=d_t_iso, updated_at=d_t_iso)
        self.assertEqual(Am.id, "678")
        self.assertEqual(Am.created_at, d_t)
        self.assertEqual(Am.created_at, d_t)

    def test_instantiating_withNone_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests testing hw the class Amenity is being saved/serialized"""

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

    def test_1_save(self):
        Am = Amenity()
        sleep(0.08)
        first_updated_at = Am.updated_at
        Am.save()
        self.assertLess(first_updated_at, Am.updated_at)

    def test_2_saves(self):
        Am = Amenity()
        sleep(0.08)
        first_updated_at = Am.updated_at
        Am.save()
        second_updated_at = Am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.08)
        Am.save()
        self.assertLess(second_updated_at, Am.updated_at)

    def test_save_witharguments(self):
        Am = Amenity()
        with self.assertRaises(TypeError):
            Am.save(None)

    def test_save_updating_file(self):
        Am = Amenity()
        Am.save()
        Am_id = "Amenity." + Am.id
        with open("file.json", "r") as f:
            self.assertIn(Am_id, f.read())


class TestAmenity_to_dictionary(unittest.TestCase):
    """Unittest testing to_dict method of the Subclass Amenity"""

    def test_typeof_to_dict(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_containg_right_keys(self):
        Am = Amenity()
        self.assertIn("id", Am.to_dict())
        self.assertIn("created_at", Am.to_dict())
        self.assertIn("updated_at", Am.to_dict())
        self.assertIn("__class__", Am.to_dict())

    def test_to_dict_containing_added_attributes(self):
        Am = Amenity()
        Am.nickname = "Reginah"
        Am.fav_no = 44
        self.assertEqual("Reginah", Am.nickname)
        self.assertIn("fav_no", Am.to_dict())

    def test_to_dict_id_and_datetime_attr_are_str(self):
        Am = Amenity()
        Am_dict = Am.to_dict()
        self.assertEqual(str, type(Am_dict["id"]))
        self.assertEqual(str, type(Am_dict["created_at"]))
        self.assertEqual(str, type(Am_dict["updated_at"]))

    def test_output_of_to_dict(self):
        d_t = datetime.now()
        Am = Amenity()
        Am.id = "456789"
        Am.created_at = Am.updated_at = d_t
        time_dict = {
            'id': '456789',
            '__class__': 'Amenity',
            'created_at': d_t.isoformat(),
            'updated_at': d_t.isoformat(),
        }
        self.assertDictEqual(Am.to_dict(), time_dict)

    def test_contrat_to_dict_and__dict__(self):
        Am = Amenity()
        self.assertNotEqual(Am.to_dict(), Am.__dict__)

    def test_to_dict_withargs(self):
        Am = Amenity()
        with self.assertRaises(TypeError):
            Am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
