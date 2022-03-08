from ..holder import FunctionHolder


def test_add_function():
    init_count = FunctionHolder.functions_count()

    @FunctionHolder.shell_function('test_add_function')
    def fun():
        return 228

    assert FunctionHolder.functions_count() == init_count + 1


def test_unknown_function():
    assert FunctionHolder.get_function('function_with_new_name_123456') is None


def test_correct_function():
    @FunctionHolder.shell_function('test_correct_function')
    def fun():
        return 322

    function = FunctionHolder.get_function('test_correct_function')

    assert function is not None
    assert function() == 322


def test_add_multiple_functions():
    init_count = FunctionHolder.functions_count()

    for i in range(100):
        @FunctionHolder.shell_function(f'test_add_multiple_functions_{i}')
        def fun():
            return i ** 2

        assert FunctionHolder.functions_count() == init_count + (i + 1)

        function = FunctionHolder.get_function(f'test_add_multiple_functions_{i}')

        assert function is not None
        assert function() == i ** 2


def test_multiple_calls():
    init_count = FunctionHolder.functions_count()

    @FunctionHolder.shell_function('test_multiple_calls')
    def fun():
        return 1337

    for _ in range(10):
        function = FunctionHolder.get_function('test_multiple_calls')

        assert function is not None
        assert function() == 1337

    assert FunctionHolder.functions_count() == init_count + 1
