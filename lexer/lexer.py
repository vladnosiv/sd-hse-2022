import re
import ply.lex as lex


class Lexer:

    tokens = (
        'pipe',
        'assign',
        'exit_token',
        'word'
    )

    # для каждого токена из массива мы должны написать его определение вида t_ИМЯТОКЕНА = регулярка
    t_pipe = r'\|'
    t_assign = r'='
    t_exit_token = r'exit'
    t_word = r'[$._a-zA-Z0-9\'"]+'

    t_ignore = ' \r\n\t\f'

    def t_error(self, t):
        pass

    def __init__(self):
        self.lexer = lex.lex(module=self)
