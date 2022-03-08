from plys.ply.yacc import yacc
from lexer import Lexer
import re


class CommandParser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'pipe'),
    )

    def p_command(self, p):
        '''
        command : command pipe command
                | assign
                | atom
                | pipe_error
                | assign_error
        '''

        if len(p) == 4 and p[2] == '|':
            p[0] = ('pipe', p[1], p[3])
        else:
            p[0] = p[1]

    def p_pipe_error(self, p):
        '''
        pipe_error : command pipe
                   | pipe command
        '''

        if p[1] == '|':
            raise ParserException("Pipe's left command can't be empty")
        else:
            raise ParserException("Pipe's right command can't be empty")

    def p_assign_error(self, p):
        '''
        assign_error : word assign
                     | assign word
        '''

        if p[1] == '=':
            raise ParserException("Variables can't have an empty name")
        else:
            raise ParserException("Can't assign empty value")

    def p_assign(self, p):
        '''
        assign : assignment
        '''

        var = self.__remove_quotes(p[1][0])
        val = self.__remove_quotes(p[1][1])
        p[0] = ('assign', var, val)

    def p_atom(self, p):
        '''
        atom : word args
             | word
        '''

        p[1] = self.__remove_quotes(p[1])
        if len(p) == 3:
            p[0] = ('func_with_args', p[1], p[2])
        else:
            p[0] = ('func', p[1])

    def p_args(self, p):
        '''
        args : word args
             | word
        '''

        p[1] = self.__remove_quotes(p[1])
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_error(self, p):
        if p.value == '|':
            raise ParserException("Wrong pipe usage")
        elif p.value == '=':
            raise ParserException("Wrong assignment usage")
        else:
            raise ParserException(f"Wrong '{p.value}' usage")

    def __remove_quotes(self, string: str) -> str:
        """
        Removes pairing quotes in a string if they exists.
        :param string: an input string
        :returns: a string without pairing quotes
        :raises ParserException: if the input has incorrect quoting
        """

        new_string = []
        open_strong = False
        open_weak = False

        for c in string:
            if c == "'" and not open_weak:
                open_strong = not open_strong
            elif c == '"' and not open_strong:
                open_weak = not open_weak
            else:
                new_string.append(c)

        if open_strong:
            raise ParserException("Strong quoting without closing symbol")
        elif open_weak:
            raise ParserException("Weak quoting without closing symbol")
        else:
            return ''.join(new_string)

    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc(module=self, debug=False)

    '''
        Parses the expression using a parser assembled
        from the grammar written inside the rest of
        the class methods
    '''
    def parse(self, s):
        '''
            s: str -- parsing string
        '''

        if re.fullmatch(r'\s*', s):
            return ()
        else:
            return self.parser.parse(s)


class ParserException(Exception):
    """
    An exception raised for errors occurred while parsing command.

    Attributes:
        message -- a message explaining parsing failure
    """

    def __init__(self, message: str):
        """
        :param message: a message explaining parsing failure
        """

        self.message = message
        super().__init__(self.message)
