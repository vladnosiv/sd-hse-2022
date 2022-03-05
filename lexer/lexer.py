import re
import ply.ply.lex as lex


class Lexer:
    '''
        Class with lexer rules
        Is designed to be used inside
        the parses with the help of
        the PLY library tools
    '''
    tokens = (
        'pipe',
        'assign',
        'exit_token',
        'word',
    )

    literals = ['=']

    t_pipe = r'\|'
    t_assign = r'='
    t_exit_token = r'exit'
    t_word = r'([:\\/%._\w$\-]+|\'[^\']*\'|"[^"]*")+'

    t_ignore = ' \r\n\t\f'

    def t_error(self, t):
        pass

    def __init__(self):
        self.lexer = lex.lex(module=self)
