#!/usr/bin/python3
"""Unittests for the TestReviewDocs Classes"""

from datetime import datetime
import inspect
from models import review
from models.base_model import BaseModel
import pep8
import unittest
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests that check the documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """Sets up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)
    # This is a variable where the result of inspect.getmembers will be
    # stored.It is an attr of the class TestReviewDocs
    # inspect.getmembers is a func from the inspect module that returns all
    # members(functions) of Review class, inspec.function is a func from
    # the inspect mod that is used as a filter to determine if a member
    # is func, it takes a member as an arg and returns True if the member
    # is a function and False otherwise

    def test_pep8_confirmation_on_review(self):
        """Test that modesl/review.py conforms to pep8"""
        pep8to = pep8.StyleGuide(quiet=True)
        result = pep8to.check_files(["models/review.py"])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Tests the Review class"""
    def test_if_is_subclass(self):
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test if Review has place_id attr and its an empty str"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Tests if Review has user_id attr and its an empty str"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        self.assertEqual(review.user_id, "")

    def text_text_attr(self):
        """Test if Review has a text attr and its empty str"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        self.assertEqual(review.text, "")

    def test_to_dict(self):
        """test to_method if it creates a dict with proper attrs"""
        rv = Review()
        new_dict = rv.to_dict()
        self.assertEqual(type(new_dict), dict)
        for attr in rv.__dict__:
            self.assertTrue(attr in new_dict)
            self.assertTrue("__class__" in new_dict)

    def test_to_dict_values(self):
        """Test if the values from the to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        rv = Review()
        new_d = rv.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], rv.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], rv.updated_at.strftime(t_format))

    def test_str(self):
        """Tests that the string method works properly"""
        rv = Review()
        str_rep = "[Review] ({}) {}".format(rv.id, rv.__dict__)
        self.assertEqual(str_rep, str(rv))
