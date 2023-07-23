#!/usr/bin/python3
"""Defines unittests for models/place.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing creating instances in the Place class"""
    def test_type_noargs_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_and_str(self):
        self.assertEqual(str, type(Place().id))

    def test_if_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_if_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_cls_att(self):
        pl = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(pl))
        self.assertNotIn("city_id", pl.__dict__)

    def test_user_id_ispublic_cls_attr(self):
        pl = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(pl))
        self.assertNotIn("user_id", pl.__dict__)

    def test_name_ispublic_cls_attr(self):
        pl = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(pl))
        self.assertNotIn("name", pl.__dict__)

    def test_description_ispublic_cls_attr(self):
        pl = Place()
        self.assertEqual(str, type(Place().description))
        self.assertIn("description", dir(pl))
        self.assertNotIn("description", pl.__dict__)

    def test_number_rooms_isPublic_clsattr(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(pl))
        self.assertNotIn("number_rooms", pl.__dict__)

    def test_number_bathrooms_ispublic_clsattr(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(pl))
        self.assertNotIn("number_bathrooms", pl.__dict__)

    def test_max_guest_ispublic_clsattr(self):
        pl = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(pl))
        self.assertNotIn("max_guest", pl.__dict__)

    def test_price_by_night_ispublic_clsattr(self):
        pl = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(pl))
        self.assertNotIn("price_by_night", pl.__dict__)

    def test_latitude_ispublicinstance_cls_attr(self):
        pl = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(pl))
        self.assertNotIn("latitude", pl.__dict__)

    def test_longitude_ispublic_clsattr(self):
        pl = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(pl))
        self.assertNotIn("longitude", pl.__dict__)

    def test_amenity_id_ispublic_clsaattr(self):
        pl = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(pl))
        self.assertNotIn("amenity_ids", pl.__dict__)

    def test_2_places_unique_ids(self):
        pl = Place()
        pll = Place()
        self.assertNotEqual(pl.id, pll.id)

    def test_2places_different_created_at(self):
        pl = Place()
        sleep(0.08)
        pll = Place()
        self.assertLess(pl.created_at, pll.created_at)

    def test_2places_different_updated_at(self):
        pl = Place()
        sleep(0.08)
        pll = Place()
        self.assertLess(pl.updated_at, pll.updated_at)

    def test_str_representation(self):
        dt = datetime.now()
        dt_repr = repr(dt)
        pl = Place()
        pl.id = "456789"
        pl.created_at = pl.updated_at = dt
        pl_str = pl.__str__()
        self.assertIn("[Place] (456789)", pl_str)
        self.assertIn("'id': '456789'", pl_str)
        self.assertIn("'created_at': " + dt_repr, pl_str)
        self.assertIn("'updated_at': " + dt_repr, pl_str)

    def test_unused_args(self):
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        pl = Place(id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(pl.id, "456")
        self.assertEqual(pl.created_at, dt)
        self.assertEqual(pl.updated_at, dt)

    def test_instantiation_with_none_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_Save(unittest.TestCase):
    """Unittests for the save method in the Place Class"""

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
        pl = Place()
        sleep(0.08)
        first_updated_at = pl.updated_at
        pl.save()
        self.assertLess(first_updated_at, pl.updated_at)

    def test_save_twice(self):
        pl = Place()
        sleep(0.08)
        first_updated_at = pl.updated_at
        pl.save()
        second_updated_at = pl.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.08)
        pl.save()
        self.assertLess(second_updated_at, pl.updated_at)

    def test_save_with_args(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updating_file(self):
        pl = Place()
        pl.save()
        pl_id = "Place." + pl.id
        with open("file.json", "r") as f:
            self.assertIn(pl_id, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittest for testing to_dict on Place class"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_containing_correct_keys(self):
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())

    def test_to_dict_contains_added_attr(self):
        pl = Place()
        pl.nickname = "reggy"
        pl.fav_no = 44
        self.assertEqual("reggy", pl.nickname)
        self.assertIn("fav_no", pl.to_dict())

    def test_to_dict_datetime_attr_are_str(self):
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_output_of_to_dict(self):
        dt = datetime.now()
        pl = Place()
        pl.id = "456789"
        pl.created_at = pl.updated_at = dt
        t_dict = {
            'id': '456789',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pl.to_dict(), t_dict)

    def test_contrast_to_dict_and__dict__(self):
        pl = Place()
        self.assertNotEqual(pl.to_dict(), pl.__dict__)
        # the inequality is because to_dict provides additional functional
        # ity beyond default behaviour of the __dict_ such as transforming
        # or modifying the attr values, adding extra key-value pairs or
        # chainging the structure of the dict representation
        # peep here from baseModel cls: "rdict = self.__dict__.copy()

    def test_to_dict_wit_args(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
