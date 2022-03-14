from io import BytesIO
import tempfile
from ..functions import cat, echo, wc, pwd, shell_exit


def stream(string=''):
    return BytesIO(string.encode())


def test_cat():
    fp = tempfile.NamedTemporaryFile(dir='/tmp')
    filename = fp.name
    code, out, err = cat(stream(), filename)

    assert code == 0
    assert err.getvalue() == b''

    text = out.getvalue().decode()

    code, out, err = cat(BytesIO(), filename)

    assert code == 0
    assert err.getvalue() == b''
    assert text == out.getvalue().decode()

    code, out, err = cat(BytesIO(), 'unknown_file.hehe')
    assert code != 0


def test_echo():
    values = ['1', '2', '3', 'hehe', '1337', '14', '42']
    text = ' '.join(values)

    code, out, err = echo(stream(), *values)

    assert code == 0
    assert err.getvalue() == b''
    assert out.getvalue().decode() == text

    code, out, err = echo(stream('        '.join(values)))

    assert code == 0
    assert err.getvalue() == b''
    assert out.getvalue().decode() == text


def test_wc():
    fp = tempfile.NamedTemporaryFile(dir='/tmp')
    filename = fp.name

    code, out, err = wc(stream(), filename)

    assert code == 0
    assert err.getvalue() == b''

    text = out.getvalue().decode()

    code, out, err = wc(cat(stream(filename))[1])

    assert code == 0
    assert err.getvalue() == b''
    assert text == out.getvalue().decode()

    code, out, err = wc(stream(), filename, filename)

    assert code != 0


def test_pwd():
    code, out, err = pwd(stream())

    assert code == 0
    assert err.getvalue() == b''
