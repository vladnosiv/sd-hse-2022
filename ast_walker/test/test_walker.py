from io import BytesIO
from ..walker import ASTWalker


def stream(string=''):
    return BytesIO(string.encode())


def test_walk():
    ast = ('func_with_args', 'echo', ['"123"', '"456"'])
    code, out, err = ASTWalker.execute(ast, stream())

    assert code == 0
    assert err.getvalue() == b''
    assert out.getvalue() == b'"123" "456"\n'

