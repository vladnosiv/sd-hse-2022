from ply.ply.lex import LexError
from lexer import Lexer
import pytest


def check_tokens(lexer, true_tokens):
    tokens = []
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break
        tokens.append(tok.type)
    return tokens == true_tokens


def test_simple():
    data = 'pwd | wc'
    lexer = Lexer()
    lexer.lexer.input(data)

    assert check_tokens(lexer, [
        'word',
        'pipe',
        'word'
    ])


def test_bad_symbol():
    data = 'pwd@'
    lexer = Lexer()
    lexer.lexer.input(data)

    with pytest.raises(LexError):
        check_tokens(lexer, [])


def test_assign():
    data = "A='input.txt'"
    lexer = Lexer()
    lexer.lexer.input(data)

    assert check_tokens(lexer, [
        'word',
        'assign',
        'word'
    ])
