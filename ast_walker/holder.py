class FunctionHolder:
    __functions = dict()

    @classmethod
    def shell_function(cls, name): #decorator
        def wrapper(function):
            if name in cls.__functions:
                raise KeyError(f'function {name} already exists')

            cls.__functions[name] = function
            return function
        return wrapper

    @classmethod
    def get_function(cls, name):
        if name not in cls.__functions:
            return None

        return cls.__functions[name]

    @classmethod
    def functions_count(cls):
        return len(cls.__functions)
