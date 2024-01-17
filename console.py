#!/usr/bin/python3
"""
Module for the HBNBCommand class.
"""
import cmd
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class for handling the command-line interface.
    """

    prompt = "(hbnb) "

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it to JSON file, and prints its ID.
        Syntax: create <Class name> <param 1> <param 2> <param 3>...
        Param syntax: <key name>=<value>
        Value syntax:
            - String: "<value>" => starts with a double quote
                - any double quote inside the value must be escaped with a backslash \
                - all underscores _ must be replaced by spaces
            - Float: <unit>.<decimal> => contains a dot .
            - Integer: <number> => default case
        If any parameter doesn’t fit with these requirements or can’t be recognized correctly, it must be skipped.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        class_dict = storage.classes()[class_name].__dict__

        new_instance = storage.classes()[class_name]()

        for param in args[1:]:
            key_value = param.split('=')
            if len(key_value) == 2:
                key, value = key_value
                if key in class_dict:
                    try:
                        if value[0] == '"' and value[-1] == '"':
                            # String value
                            setattr(new_instance, key, value[1:-1].replace('_', ' '))
                        elif '.' in value:
                            # Float value
                            setattr(new_instance, key, float(value))
                        else:
                            # Integer value
                            setattr(new_instance, key, int(value))
                    except ValueError:
                        print(f"Invalid value for parameter {key}: {value}")
            else:
                print(f"Invalid parameter format: {param}")

        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_all(self, arg):
        """
        Prints all string representation of all instances based on the class name.
        Syntax: all <Class name>
        If <Class name> is not given, prints all instances.
        """
        args = arg.split()
        if not args:
            print([str(obj) for obj in storage.all().values()])
        else:
            class_name = args[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
                return
            print([str(obj) for obj in storage.all(storage.classes()[class_name]).values()])

    def do_EOF(self, line):
        """
        Exits the program gracefully.
        """
        return True

    def emptyline(self):
        """
        Handles an empty line by doing nothing (avoids repeating the last command).
        """
        pass

if __name__ == "__main__":
    HBNBCommand().cmdloop()
