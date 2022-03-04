from ..parser import CommandParser, ParserException


def test_simple():
    s = 'echo 123 | wc'
    parser = CommandParser()
    ast = parser.parse(s)

    assert ast == (
        'pipe',
        (
            'func_with_args', 'echo', ['123']
        ),
        (
            'func', 'wc'
        )
    )


def test_bad_pipe():
    s = 'pwd | wc |'
    parser = CommandParser()
    try:
        ast = parser.parse(s)
    except ParserException:
        ast = None

    assert ast is None


def test_assignment():
    s = 'afe2=DWQQW123.txt'
    parser = CommandParser()
    ast = parser.parse(s)

    assert ast == (
        'assign',
        'afe2',
        'DWQQW123.txt'
    )


