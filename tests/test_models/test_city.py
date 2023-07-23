#!/usr/bin/python3
"""Unittest for the subclass User"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """
    Unittests for testing creation of instances of the City class
    """
    def test_type_with_no_args(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(City(), models.storage.all().values())

    def test_if_id_is_public_and_str(self):
        self.assertEqual(str, type(City().id))

    def test_if_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_if_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_attr(self):
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_cls_attr(self):
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_2_cities_unique_ids(self):
        cy = City()
        cyy = City()
        self.assertNotEqual(cy.id, cyy.id)

    def test_2_cities_different_created_at(self):
        cy = City()
        sleep(0.08)
        cyy = City()
        self.assertLess(cy.created_at, cyy.created_at)

    def test_2_cities_different_updated_at(self):
        cy = City()
        sleep(0.08)
        cyy = City()
        self.assertLess(cy.updated_at, cyy.updated_at)

    def test_str_representation(self):
        d_t = datetime.now()
        d_t_repr = repr(d_t)
        cy = City()
        cy.id = "456789"
        cy.created_at = cy.updated_at = d_t
        cy_str = cy.__str__()
        self.assertIn("[City] (456789)", cy_str)
        self.assertIn("'id': '456789'", cy_str)
        self.assertIn("'created_at': " + d_t_repr, cy_str)
        self.assertIn("'updated_at': " + d_t_repr, cy_str)

    def test_unused_args(self):
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        cy = City(id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "456")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_Kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittest for the save method in the City class"""

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

    def test_save_once(self):
        cy = City()
        sleep(0.08)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_saving_twice(self):
        cy = City()
        sleep(0.08)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.08)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arguments(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updating_file(self):
        cy = City()
        cy.save()
        cy_id = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cy_id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the class City"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_containing_right_keys(self):
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def test_to_dict_containing_added_attr(self):
        cy = City()
        cy.nickname = "Shicky"
        cy.fav_no = 44
        self.assertEqual("Shicky", cy.nickname)
        self.assertIn("fav_no", cy.to_dict())

    def test_to_dict_datetime_att_are_strs(self):
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_output_of_to_dict(self):
        dt = datetime.now()
        cy = City()
        cy.id = "456789"
        cy.created_at = cy.updated_at = dt
        t_dict = {
            'id': '456789',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), t_dict)

    def test_contrast_to_dict_and__dict__(self):
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_args(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
