import re
import ply.lex as lex

class Lexer:

    tokens = (
        'pipe', 'assign', 'double_quote', 'double_quote_interior',
        'single_quote', 'single_quote_interior', 'exit_token', 'word',
        'skip_token')

    # определим регулярку для абстрактного идетификатора
    ident = r'[a-z]\w*'

    # для каждого токена из массива мы должны написать его определение вида t_ИМЯТОКЕНА = регулярка
    t_pipe = r'\|'
    t_assign = r'='
    t_double_quote = r'\"'
    t_double_quote_interior = r'\[^\"]*'
    t_single_quote = r'\''
    t_single_quote_interior = r'\[^\']*'
    t_exit_token = r'exit'
    t_word = r'[$_a-zA-Z0-9.]+'
    t_skip_token = r'[\s\t\n\r]+'

    t_ignore = ' \r\n\t\f'

    def t_error(t):
        t.value = t.lexer.lexpos
        t.lexer.skip(1)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    __lexer = lex.lex(reflags=re.UNICODE | re.DOTALL)

    def tokenize(self, str):
        self.__lexer.input(str)
        result = []
        while True:
            tok = self.__lexer.token()
            if not tok:
                break
            if tok.type == "error":
                return result, str[tok.value:]
            result.append(tok)
        return result, ""
