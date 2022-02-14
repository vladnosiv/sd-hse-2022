from ply.yacc import yacc
from lexer import Lexer


class CommandParser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'pipe'),
    )

    def p_command(self, p):
        '''
        command : command pipe command
                | assignment
                | atom
                | exit_token
        '''
        if len(p) == 4 and p[2] == '|':
            p[0] = ('pipe', p[1], p[3])
        else:
            p[0] = p[1]

    def p_assignment(self, p):
        '''
        assignment : word assign word
        '''
        p[0] = ('assign', p[1], p[3])

    def p_atom(self, p):
        '''
        atom : word args
             | word
        '''
        if len(p) == 3:
            p[0] = ('func_with_args', p[1], p[2])
        else:
            p[0] = ('func', p[1])

    def p_args(self, p):
        '''
        args : word args
             | word
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_error(self, p):
        pass

    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc(module=self)

    '''
        Parses the expression using a parser assembled
        from the grammar written inside the rest of
        the class methods
    '''
    def parse(self, s):
        '''
            s: str -- parsing string
        '''
        if s == '':
            return ()
        else:
            return self.parser.parse(s)
