import os
import copy
import re
from typing import Optional


class EnvironmentHandler:
    """
    A module that contains system variables.
    """
    __vars = copy.deepcopy(dict(os.environ))

    @classmethod
    def set_value(cls, name: str, value: str):
        """
        Sets a new value for a variable.
        :param name: a variable's name as a string
        :param value: a new value as a string
        """

        cls.__vars[name] = value

    @classmethod
    def get_value(cls, name: str) -> str:
        """
        Returns variable's value.
        :param name: a variable's name as a string
        :returns: a variable's value as a string if it exists, an empty string if not
        """

        return cls.__vars.get(name, '')

    @classmethod
    def as_dict(cls):
        return cls.__vars



class Substitute():
    """
    A module with system variables that handles substitution and assignment commands.
    """

    def deref(self, command: str) -> str:
        """
        Replaces variables names to their values in a command. Supports strong and weak quoting.
        A variable name found in an input if '$' stays before it.
        :param command: an input command as a string
        :returns: a command with substitutions
        :raises SubstituteException: if the input has incorrect quoting or '$' usage
        """

        string = command
        new_string = []
        open_strong = False
        open_weak = False
        curr_var = []

        for c in string:
            if c == "'" and not open_weak:
                open_strong = not open_strong

                if len(curr_var) == 0:
                    new_string.append("'")
                elif len(curr_var) == 1:
                    raise SubstituteException("Variable name can't start with quotes")
                else:
                    var = ''.join(curr_var[1:])
                    val = EnvironmentHandler.get_value(var)
                    curr_var = []
                    new_string += val
                    new_string.append("'")
            elif c == '"' and not open_strong:
                open_weak = not open_weak

                if len(curr_var) == 0:
                    new_string.append('"')
                elif len(curr_var) == 1:
                    raise SubstituteException("Variable name can't start with quotes")
                else:
                    var = ''.join(curr_var[1:])
                    val = EnvironmentHandler.get_value(var)
                    curr_var = []
                    new_string += val
                    new_string.append('"')
            elif c == '$' and not open_strong:
                if len(curr_var) == 0:
                    curr_var.append('$')
                elif len(curr_var) == 1:
                    raise SubstituteException("Variable name can't start with '$'")
                else:
                    var = ''.join(curr_var[1:])
                    val = EnvironmentHandler.get_value(var)
                    curr_var = ['$']
                    new_string += val
            elif re.match(r'[_\w\-0-9]', c) is None:
                if len(curr_var) == 0:
                    new_string.append(c)
                elif len(curr_var) == 1:
                    raise SubstituteException(f"Variable name can't start with '{c}'")
                else:
                    var = ''.join(curr_var[1:])
                    val = EnvironmentHandler.get_value(var)
                    curr_var = []
                    new_string += val
                    new_string.append(c)
            elif re.match(r'[0-9]', c) is not None and len(curr_var) == 1:
                raise SubstituteException(f"Variable name can't start with digit") 
            else:
                if len(curr_var) > 0:
                    curr_var.append(c)
                else:
                    new_string.append(c)

        if len(curr_var) == 1:
            raise SubstituteException("Variable name can't be empty")
        elif len(curr_var) > 1:
            var = ''.join(curr_var[1:])
            val = EnvironmentHandler.get_value(var)
            new_string += val

        if open_strong:
            raise SubstituteException("Strong quoting without closing symbol")
        elif open_weak:
            raise SubstituteException("Weak quoting without closing symbol")
        else:
            return ''.join(new_string)


class SubstituteException(Exception):
    """
    An exception raised for errors occurred while parsing substitutuions.

    Attributes:
        message -- a message explaining parsing failure
    """

    def __init__(self, message: str):
        """
        :param message: a message explaining parsing failure
        """

        self.message = message
        super().__init__(self.message)
