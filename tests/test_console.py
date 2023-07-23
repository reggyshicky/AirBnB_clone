#!/usr/bin/python3
"""Module unittests for console.py
Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import unittest
import os
import sys
from unittest.mock import patch
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for HBNB comand interpreter"""

    def test_prompt_str(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Test case for HBNB interpreter"""

    def test_helpQuit(self):
        m = "Exit/Quits the console when executed"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpCreate(self):
        m = ("Creates a new class instance and prints its id")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpEOF(self):
        m = "EOF signals the exit of the program/"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpShow(self):
        m = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpDestroy(self):
        m = ("Deletes an instance based on the class name and instance id")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpAll(self):
        m = ("Prints all string representation of all instances based or not\n"
             "        on the class name")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpCount(self):
        m = ("Retrieves the number of instances of a class")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(m, output.getvalue().strip())

    def test_helpUpdate(self):
        m = ("Updates an instance based on the cls name and instance id by\n"
             "        adding or updating an attribute")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(m, output.getvalue().strip())

    def test_help(self):
        m = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(m, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittest for testing exit command"""

    def test_exit_quit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_exit_EOF(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unitest for create HBNB interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missingClass(self):
        m = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(m, output.getvalue().strip())

    def test_create_invalidClass(self):
        m = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(m, output.getvalue().strip())

    def test_create_invalidSyntax(self):
        m = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(m, output.getvalue().strip())
        m = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(m, output.getvalue().strip())

    def test_create_obj(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "User.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "State.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "City.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "Place.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            keytest = "Review.{}".format(output.getvalue().strip())
            self.assertIn(keytest, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittest to test for show for HNB command intepreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_missingClass(self):
        m = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_invalidClass(self):
        m = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_missing_idSpaceNotation(self):
        m = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_missing_idDotNotation(self):
        m = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_noInstanceFoundSpaceNotation(self):
        m = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_noInstanceFoundDotNotation(self):
        m = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(m, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(m, output.getvalue().strip())

    def test_show_objSpaceNotations(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(IDtest)]
            cmd_1 = "show BaseModel {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(IDtest)]
            cmd_1 = "show User {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(IDtest)]
            cmd_1 = "show State {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(IDtest)]
            cmd_1 = "show City {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(IDtest)]
            cmd_1 = "show Amenity {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(IDtest)]
            cmd_1 = "show Place {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(IDtest)]
            cmd_1 = "show Review {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(IDtest)]
            cmd_1 = "BaseModel.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(IDtest)]
            cmd_1 = "User.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(IDtest)]
            cmd_1 = "State.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(IDtest)]
            cmd_1 = "City.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(IDtest)]
            cmd_1 = "Amenity.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(IDtest)]
            cmd_1 = "Place.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(IDtest)]
            cmd_1 = "Review.show({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unitest for destroy HBNB console command"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def test_destroy_missingClass(self):
        right = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_invalidClass(self):
        right = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_idMissingSpaceNotation(self):
        right = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_idMissingDotNotation(self):
        right = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_invalidIdSpaceNotation(self):
        right = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_invalidDotNotation(self):
        right = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(right, output.getvalue().strip())

    def test_destroy_objSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(IDtest)]
            cmd_1 = "destroy BaseModel {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(IDtest)]
            cmd_1 = "destroy User {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(IDtest)]
            cmd_1 = "destroy State {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(IDtest)]
            cmd_1 = "destroy City {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(IDtest)]
            cmd_1 = "destroy Amenity {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(IDtest)]
            cmd_1 = "destroy Place {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(IDtest)]
            cmd_1 = "destroy Review {}".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(IDtest)]
            cmd_1 = "BaseModel.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(IDtest)]
            cmd_1 = "User.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(IDtest)]
            cmd_1 = "State.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(IDtest)]
            cmd_1 = "City.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(IDtest)]
            cmd_1 = "Amenity.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(IDtest)]
            cmd_1 = "Place.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            IDtest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(IDtest)]
            cmd_1 = "Review.destroy({})".format(IDtest)
            self.assertFalse(HBNBCommand().onecmd(cmd_1))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_all_invalidClass(self):
        right = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_all_objSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def test_all_ojDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def test_all_singleObjSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_singleObjDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """unittest for testing update for HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_missingClass(self):
        right = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_invalidClass(self):
        right = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingIdSpaceNotation(self):
        right = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingIdDotNotation(self):
        right = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_invalidIdSpaceNotation(self):
        right = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_invalidIdDotNotation(self):
        right = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingAttrNameSpaceNotation(self):
        right = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            idTest = output.getvalue().strip()
            cmdTest = "update BaseModel {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            idTest = output.getvalue().strip()
            cmdTest = "update User {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            idTest = output.getvalue().strip()
            cmdTest = "update State {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            idTest = output.getvalue().strip()
            cmdTest = "update City {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            idTest = output.getvalue().strip()
            cmdTest = "update Amenity {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            idTest = output.getvalue().strip()
            cmdTest = "update Place {}".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingAttrNameDotNotation(self):
        right = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            idTest = output.getvalue().strip()
            cmdTest = "BaseModel.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            idTest = output.getvalue().strip()
            cmdTest = "User.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            idTest = output.getvalue().strip()
            cmdTest = "State.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            idTest = output.getvalue().strip()
            cmdTest = "City.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            idTest = output.getvalue().strip()
            cmdTest = "Amenity.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            idTest = output.getvalue().strip()
            cmdTest = "Place.update({})".format(idTest)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingAttrValueSpaceNotation(self):
        right = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update BaseModel {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update User {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update State {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update City {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update Amenity {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update Place {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "update Review {} name_attr".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_missingAttrValueDotNotation(self):
        right = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "BaseModel.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "User.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "State.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "City.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "Amenity.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "Place.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            cmdTest = "Review.update({}, name_attr)".format(idTest)
            self.assertFalse(HBNBCommand().onecmd(cmdTest))
            self.assertEqual(right, output.getvalue().strip())

    def test_update_validStrAttrSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        cmdTest = "update BaseModel {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["BaseModel.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        cmdTest = "update User {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["User.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        cmdTest = "update State {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["State.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        cmdTest = "update City {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["City.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        cmdTest = "update Amenity {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Amenity.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        cmdTest = "update Review {} name_attr 'value_attr'".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Review.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

    def test_update_validStrAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        cmdTest = "BaseModel.update({}, name_atr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["BaseModel.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_atr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        cmdTest = "User.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["User.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        cmdTest = "State.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["State.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        cmdTest = "City.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["City.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        cmdTest = "Amenity.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Amenity.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        cmdTest = "Review.update({}, name_attr, 'value_attr')".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Review.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

    def test_update_validIntAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} max_guest 98)".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(98, dict_test["max_guest"])

    def test_update_validIntAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}, max_guest, 98)".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(98, dict_test["max_guest"])

    def test_update_validFloatAttrSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} latitude 7.2".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(7.2, dict_test["latitude"])

    def test_update_validFloatAttrDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}, latitude, 7.2)".format(idTest)
        self.assertFalse(HBNBCommand().onecmd(cmdTest))
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(7.2, dict_test["latitude"])

    def test_update_validDictSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        cmdTest = "update BaseModel {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["BaseModel.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        cmdTest = "update User {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["User.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        cmdTest = "update State {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["State.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        cmdTest = "update City {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["City.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        cmdTest = "update Amenity {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Amenity.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        cmdTest = "update Review {} ".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Review.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

    def test_update_validDictDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            idTest = output.getvalue().strip()
        cmdTest = "BaseModel.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["BaseModel.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            idTest = output.getvalue().strip()
        cmdTest = "User.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["User.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            idTest = output.getvalue().strip()
        cmdTest = "State.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["State.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            idTest = output.getvalue().strip()
        cmdTest = "City.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["City.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            idTest = output.getvalue().strip()
        cmdTest = "Amenity.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Amenity.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            idTest = output.getvalue().strip()
        cmdTest = "Review.update({}".format(idTest)
        cmdTest += "{'name_attr': 'value_attr'})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Review.{}".format(idTest)].__dict__
        self.assertEqual("value_attr", dict_test["name_attr"])

    def test_update_validDictWithIntSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} ".format(idTest)
        cmdTest += "{'max_guest': 98}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(98, dict_test["max_guest"])

    def test_update_validDictWithIntDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}, ".format(idTest)
        cmdTest += "{'max_guest': 98})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(98, dict_test["max_guest"])

    def test_update_validDictWithFloatSpaceNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "update Place {} ".format(idTest)
        cmdTest += "{'latitude': 9.8}"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(9.8, dict_test["latitude"])

    def test_update_validDictWithFloatDotNotation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            idTest = output.getvalue().strip()
        cmdTest = "Place.update({}, ".format(idTest)
        cmdTest += "{'latitude': 9.8})"
        HBNBCommand().onecmd(cmdTest)
        dict_test = storage.all()["Place.{}".format(idTest)].__dict__
        self.assertEqual(9.8, dict_test["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for count of HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_invalidClass(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def test_count_obj(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
