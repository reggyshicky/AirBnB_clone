#!/usr/bin/python3
"""Module Documentation for our Airbnb Console"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curlies = re.search(r"\{(.*?)\}", arg)
    sq_brackets = re.search(r"\[(.*?)\]", arg)

    if curlies is None:
        if sq_brackets is None:
            for token in split(arg):
                return [token.strip(",") for token in split(arg)]
        else:
            b4_brackets = split(arg[:sq_brackets.span()[0]])
            b4_brackets1 = [token.strip(",") for token in b4_brackets]
            b4_brackets1.append(sq_brackets.group())
            return b4_brackets1
    else:
        b4_brackets = split(arg[:curlies.span()[0]])
        b4_brackets1 = [token.strip(",") for token in b4_brackets]
        b4_brackets1.append(curlies.group())
        return b4_brackets1
    return []


class HBNBCommand(cmd.Cmd):
    """Defines our Airbnb Console"""
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Does not execute anything when the line is empty"""
        pass

    def default(self, arg):
        """
        method called on an input line when the command prefix
        is not recognized
        """
        dict_args = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        matches = re.search(r"\.", arg)
        if matches is not None:
            arg_1 = [arg[:matches.span()[0]], arg[matches.span()[1]:]]
            matches = re.search(r"\((.*?)\)", arg_1[1])
            if matches is not None:
                _cmd = [arg_1[1][:matches.span()[0]], matches.group()[1:-1]]
                if _cmd[0] in dict_args.keys():
                    _call = "{} {}".format(arg_1[0], _cmd[1])
                    return dict_args[_cmd[0]](_call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Exit/Quits the console when executed"""
        return True

    def do_EOF(self, arg):
        """EOF signals the exit of the program/"""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new class instance and prints its id"""
        arg_1 = parse(arg)
        if len(arg_1) == 0:
            print("** class name missing **")
        elif arg_1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_1[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_1 = parse(arg)
        obj_dict = storage.all()
        if len(arg_1) == 0:
            print("** class name missing **")
        elif arg_1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_1[0], arg_1[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_1[0], arg_1[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and instance id"""
        arg_1 = parse(arg)
        obj_dict = storage.all()
        if len(arg_1) == 0:
            print("** class name missing **")
        elif arg_1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_1[0], arg_1[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_1[0], arg_1[1])]
            storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not
        on the class name
        """
        arg_1 = parse(arg)
        if len(arg_1) > 0 and arg_1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_1 = []
            for obj in storage.all().values():
                if len(arg_1) > 0 and arg_1[0] == obj.__class__.__name__:
                    obj_1.append(obj.__str__())
                elif len(arg_1) == 0:
                    obj_1.append(obj.__str__())
            print(obj_1)

    def do_count(self, arg):
        """Retrieves the number of instances of a class"""
        arg_1 = parse(arg)
        tally = 0
        for _obj in storage.all().values():
            if arg_1[0] == _obj.__class__.__name__:
                tally += 1
        print(tally)

    def do_update(self, arg):
        """
        Updates an instance based on the cls name and instance id by
        adding or updating an attribute
        """
        arg_1 = parse(arg)
        obj_dict = storage.all()

        if len(arg_1) == 0:
            print("** class name missing **")
            return False
        # False indicates do_all encountered an error and did not
        # execute succesfully
        if arg_1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_1[0], arg_1[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_1) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_1) == 3:
            try:
                type(eval(arg_1[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_1) == 4:
            obj = obj_dict["{}.{}".format(arg_1[0], arg_1[1])]
            if arg_1[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_1[2]])
                obj.__dict__[arg_1[2]] = val_type(arg_1[3])
            else:
                obj.__dict__[arg_1[2]] = arg_1[3]
        elif type(eval(arg_1[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_1[0], arg_1[1])]
            for k, v in eval(arg_1[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = val_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
