#!/usr/bin/python3
"""
This module provides a command-line interface (CLI) for interacting with
the AirBnB project models representing various methods for managing
the system. It allows users to apply CRUD operations
on the instances through the console.

The console offers the following functionalities:

- Creating new instances of various classes.
> create User | User.create()
- Display all available instances.
> all | all User
- Showing information about existing instances based on class and id.
> show User <id> | User.show(<id>)
- Updating existing instances by adding or modifying their attributes.
> update User <id> (args | kwargs)| User.update(<id>, (args | kwargs))
- Deleting existing instances from the storage.
> destroy User <id> | User.destroy(<id>)
- Counting the number of instances for each class.
> count all | count User
"""
import cmd
import sys
from typing import TypedDict
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


# for auto-completion
class ErrorMessages(TypedDict):
    no_method: str
    no_cls: str
    no_c_name: str
    no_obj_id: str
    no_obj: str
    no_attr_name: str
    no_attr_value: str
    no_json: str


error_messages: ErrorMessages = {
    "no_method": "** invalid method",
    "no_cls": "** class doesn't exist **",
    "no_c_name": "** class name missing **",
    "no_obj_id": "** instance id missing **",
    "no_obj": "** no instance found **",
    "no_attr_name": "** attribute name missing **",
    "no_attr_value": "** value missing **",
    "no_json": "** invalid json object **",
}

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review,
}

types = {
    'number_rooms': int,
    'number_bathrooms': int,
    'max_guest': int,
    'price_by_night': int,
    'latitude': float,
    'longitude': float,
}


class HBNBCommand(cmd.Cmd):
    """
    Command-line interface for interacting with BaseModel instances.

    This class provides a user interface for interacting with the system
    through text commands. It parses user input, validates arguments, and
    delegates tasks to appropriate methods for CRUD (Create, Read, Update,
    Delete) operations on BaseModel instances.

    The class inherits from `cmd.Cmd` from the `cmd` module, providing
    functionalities for handling user input and interactions within the
    console.
    """

    intro = "Welcome to Airbnb console.\tType help or ? to list commands.\n"
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """
        Handles cases where user commands are not recognized by HBNBCommand.

        This method is invoked when the user enters a command
        that doesn't match any of the defined functionalities in HBNBCommand.
        It checks for a pattern matching "<class_name>.<method>(<args>)"
        and attempts to call the corresponding do_* method if valid.
        Otherwise, it prints an error message.

        Args:
        -   line (str): The user input command string.

        Example:
        >> (hbnb) User.update(some_user_id, {"name": "abc"})
        >> 'update User 7993cdd5-1218-44dc-813e-97594bc228ba {"name": "abc"}'
        """
        allowed_methods = [
            'create',
            'all',
            'count',
            'show',
            'destroy',
            'update',
        ]

        _cmd = _cls = _id = _args = ''

        # check against general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        pline = line[:]  # processed line
        _cls = pline[: pline.find('.')]  # get class name
        cmd_starting_idx = pline.find('.') + 1
        cmd_ending_idx = pline.find('(')
        _cmd = pline[cmd_starting_idx:cmd_ending_idx]  # get method name
        if _cmd not in allowed_methods:
            print(f"{error_messages['no_method']}: {_cmd} **")
            return ''

        try:
            args_starting_idx = pline.find('(') + 1
            args_ending_idx = pline.find(')')
            pline = pline[args_starting_idx:args_ending_idx]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].strip("\"'")  # get instance id
                pline = pline[2].strip()  # get args i.e attributes
                if pline:
                    if (  # determine if attributes are in kwargs format
                        pline[0] == '{'
                        and pline[-1] == '}'
                        and type(eval(pline)) is dict
                    ):
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as e:
            pass
        return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, arg):
        """Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        return True

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance, and saves it a JSON file.

        Args:
        -   arg (str): The user input argument (command to be interpreted).

        Return:
        -   None (prints the created instance id on success).

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(arg, get_params=True)
        if not args:
            return

        c_name = args["c_name"]  # get class name

        obj = classes[c_name]()
        # Extra feature:
        obj_dict = dir(obj)
        allowed_params = [
            attr
            for attr in obj_dict
            if not callable(getattr(obj, attr))  # Exclude methods
            and not isinstance(
                getattr(type(obj), attr, None), property
            )  # Exclude properties
            and not attr.startswith("__")  # Exclude private attributes
        ]

        params = args["params"].split()  # [<key>="<value>", ...]

        for param in params:
            if '=' not in param:  # Skip this checks and just create the object
                continue
            param = param.split("=")
            param_name = param[0]
            # 💀 Potential checker error here 👇
            if param_name not in allowed_params:
                print(f"** invalid param for class {c_name}: <{param_name}>")
                print(f"** available params: {allowed_params}")
                return
            param_value = (
                param[1].strip("\"'").replace('"', '').replace('_', ' ')
                if len(param) > 1
                else ''
            )
            if not param_value:
                print(error_messages["no_attr_value"])
                return
            if param_name in types:
                param_value = types[param_name](param_value)
            obj.__dict__.update({param_name: param_value})

        obj.save()
        print(obj.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and its id.

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        -   check_id (bool):
                If True, checks if an instance id is provided.
                (defaults to True)

        Return:
        -   None (prints the instance id on success).

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(arg, check_id=True)
        if not args:
            return

        c_name = args["c_name"]
        obj_id = args["obj_id"]
        all_objs = storage.all()
        key = f"{c_name}.{obj_id}"
        obj = all_objs.get(key)

        if obj is None:
            print(error_messages["no_obj"])
            return
        print(obj)

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and provided instance id
        (saves the change into the JSON file).

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        -   check_id (bool): Checks if an instance id is provided
                                (defaults to True)
        """
        args = validate(arg, check_id=True)
        if not args:
            return

        c_name = args["c_name"]
        obj_id = args["obj_id"]

        objs = storage.all()
        key = f"{c_name}.{obj_id}"
        removed_obj = objs.pop(key, None)
        if removed_obj is None:
            print(error_messages["no_obj"])
            return

        storage.save()

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """
        Prints a string representation of all instances.

        Args:
        -   arg (str): The user input argument (command to be interpreted).

        Return:
        -   None (prints all the instances or empty []).

        Raises:
        -   None (prints error messages to the console).
        """
        args = arg.split()
        c_name = args[0].strip("'\"") if args else ""

        if c_name and c_name not in classes:
            print(error_messages["no_cls"])
            return

        obj_dict = {}
        if not c_name:
            obj_dict = storage.all()
        else:
            obj_dict = storage.all(cls=c_name)

        objs = [obj.__str__() for obj in obj_dict.values()]
        print(objs)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, arg):
        """
        Count the number of instance for each class.

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        """
        args = validate(arg)
        if not args:
            return

        nm_instances = 0
        objs = storage.all()
        for obj in objs.values():
            nm_instances += (
                1
                if arg == "all" or obj.__class__.__name__ == args["c_name"]
                else 0
            )
        print(nm_instances)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and its id.

        Args:
        -   arg (str): The user input argument (command to be interpreted).

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(arg, check_id=True)
        if args is None:
            return

        c_id = args["obj_id"]
        c_name = args["c_name"]
        attributes = args["attributes"][0]

        key = f"{c_name}.{c_id}"

        if key not in storage.all():
            print(error_messages["no_obj"])
            return

        obj = storage.all()[key]

        # determine if attributes are kwargs or args
        if (
            '{' in attributes
            and '}' in attributes
            and type(eval(attributes)) is dict
        ):  # attributes are in kwargs format e.g {"key": "value", ...}
            args = eval(attributes)
            attributes = [k_v for pairs in args.items() for k_v in pairs]
        else:  # attributes are in args format e.g "key", "value" ...
            attributes = attributes.split()

        for i, attr_name in enumerate(attributes or [""]):
            attr_name = (
                attr_name.strip("\"',") if type(attr_name) is str else ""
            )
            if i % 2 == 0:
                attr_value = (
                    (
                        attributes[i + 1].strip("\"',")  # Value is Str
                        if type(attributes[i + 1]) is str
                        else attributes[i + 1]  # Value is Int
                    )
                    if len(attributes) > i + 1  # Value exist
                    else ""
                )
                if not attr_name:
                    print(error_messages["no_attr_name"])
                    return
                if not attr_value:
                    print(error_messages["no_attr_value"])
                    return
                if attr_name in types:
                    attr_value = types[attr_name](attr_value)
                obj.__dict__[attr_name] = attr_value
        # save to storage
        obj.save()

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attrName> <attrValue>\n")


def validate(arg="", **kwargs):
    """
    Validates user input arguments for the HBNBCommand methods.

    This function parses the user input arguments (`arg`) and performs
    various checks based on the provided keyword arguments (`kwargs`).

    Args:
    -   arg (str): The user input argument (command to be interpreted).
    -   **kwargs (dict): Keyword arguments specifying additional validations.
            - check_id (bool):
                If True, checks if an instance id is provided.
                (defaults to False)

    Returns:
    -   dict: A (dict) containing parsed arguments on successful validation,
            (None) otherwise.

    Raises:
    -   None (prints error messages to the console).
    """
    args = arg.partition(" ")
    c_name = args[0]
    if not c_name:
        print(error_messages["no_c_name"])
        return
    if c_name not in classes and c_name != "all":
        print(error_messages["no_cls"])
        return

    if kwargs.get("get_params"):
        return {"c_name": c_name, "params": args[2]}

    args = args[2].partition(" ")
    obj_id = args[0]
    if not obj_id and kwargs.get("check_id"):
        print(error_messages["no_obj_id"])
        return

    return {"obj_id": obj_id, "c_name": c_name, "attributes": args[2:]}


if __name__ == "__main__":
    HBNBCommand().cmdloop()
