from io import BytesIO
from ..executor import FunctionExecutor


def stream(string=''):
    return BytesIO(string.encode())


def test_execution():
    code, out, err = FunctionExecutor.execute_function('echo', stream(), '228', '322')

    assert code == 0
    assert err.getvalue() == b''
    assert out.getvalue() == b'228 322\n'
