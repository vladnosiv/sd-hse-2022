class FunctionHolder:
    '''
        a class that stores functions that can be called from the CLI
    '''
    __functions = dict()

    @classmethod
    def shell_function(cls, name):  # decorator
        '''
            a decorator that allows you to turn a custom function into a function for the CLI
        '''
        def wrapper(function):
            if name in cls.__functions:
                raise KeyError(f'function {name} already exists')

            cls.__functions[name] = function
            return function
        return wrapper

    @classmethod
    def get_function(cls, name):
        '''
            name:str - function name
            returns a function or None if no function with the same name has been added
        '''
        if name not in cls.__functions:
            return None

        return cls.__functions[name]

    @classmethod
    def functions_count(cls):
        '''
            returns the number of added functions
        '''
        return len(cls.__functions)
