#!/usr/bin/python3
"""Module documentation for the State Class unittests"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittest for creating instances of the State Class"""
    def test_type_no_args_instantiating(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stores_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_ispublic_and_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_ispublictype_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_cls_attr(self):
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)
        # Assertions ensure that name is a public cls attr of the State
        # cls accessible from the st instance but not an instance attr
        # specific to the instance

    def test_2_states_unique_ids(self):
        st = State()
        stt = State()
        self.assertNotEqual(st.id, stt.id)

    def test_2_states_different_created_at(self):
        st = State()
        sleep(0.08)
        stt = State()
        self.assertLess(st.created_at, stt.created_at)

    def test_2_states_differnet_updated_at(self):
        st = State()
        sleep(0.08)
        stt = State()
        self.assertLess(st.updated_at, stt.updated_at)

    def test_str_repr(self):
        dt = datetime.now()
        dt_repr = repr(dt)
        st = State()
        st.id = "456789"
        st.created_at = st.updated_at = dt
        st_str = st.__str__()
        self.assertIn("[State] (456789)", st_str)
        self.assertIn("'id': '456789'", st_str)
        self.assertIn("'created_at': " + dt_repr, st_str)
        self.assertIn("'updated_at': " + dt_repr, st_str)

    def test_unused_args(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        st = State(id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "456")
        self.assertEqual(st.created_at, dt)
        self.assertEqual(st.updated_at, dt)

    def test_instantiation_with_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittest for the save  method in thw State class"""

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
        st = State()
        sleep(0.08)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def test_save_twice(self):
        st = State()
        sleep(0.08)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.08)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def test_save_with_args(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_save_updating_file(self):
        st = State()
        st.save()
        st_id = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(st_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing the State class to_dict method"""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_containing_correct_keys(self):
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())
        self.assertIn("__class__", st.to_dict())

    def test_to_dict_containing_added_attr(self):
        st = State()
        st.nickname = "Shicky"
        st.fav_no = 44
        self.assertEqual("Shicky", st.nickname)
        self.assertIn("fav_no", st.to_dict())

    def test_to_dict_datetime_attr_are_str(self):
        st = State()
        st_dict = st.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_oputput_of_the_to_dict(self):
        dt = datetime.now()
        st = State()
        st.id = "456789"
        st.created_at = st.updated_at = dt
        t_dict = {
            'id': '456789',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), t_dict)

    def test_contrast_to_dict_and__dict__(self):
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def test_to_dict_with_arg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
