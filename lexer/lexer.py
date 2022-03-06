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
        'assignment',
        'word',
    )

    def t_pipe(self, t):
        r'\|'
        return t

    def t_assignment(self, t):
        r'^\s*[_\w\-]+[_\w\-0-9]*=([^\s\'"]+|\'[^\']*\'|"[^"]*")+\s*$'

        var = re.search(r'[_\w\-]+[_\w\-0-9]*', t.value)[0]
        a_val = re.search(r'=\s*([^\s\'"]+|\'[^\']*\'|"[^"]*")+', t.value)[0]
        prefix = re.search(r'=\s*', a_val)[0]
        val = a_val[len(prefix):]

        t.value = (var, val)

        return t

    def t_word(self, t):
        r'([^\s\'"]+|\'[^\']*\'|"[^"]*")+'
        return t

    t_ignore = ' \r\n\t\f'

    def t_error(self, t):
        pass

    def __init__(self):
        self.lexer = lex.lex(module=self)
