from io import BytesIO
import tempfile
from ..functions import cat, echo, wc, pwd, shell_exit


def stream(string=''):
    return BytesIO(string.encode())


def get_temp_file(content=None):
    fp = tempfile.NamedTemporaryFile(dir='/tmp', delete=False)
    filename = fp.name

    if content is not None:
        with open(filename, 'w') as f:
            f.write(content)

    return filename


def function_test(function, expected_code, expected_out=None, expected_err=None):
    code, out, err = function()

    if expected_code == 'zero':
        assert code == 0
    elif expected_code == 'non zero':
        assert code != 0

    if expected_err is not None:
        assert err.getvalue() == expected_err.encode()

    if expected_out is not None:
        assert out.getvalue() == expected_out.encode()


def test_cat_one_file():
    fp = tempfile.NamedTemporaryFile(dir='/tmp')
    filename = fp.name

    file_content = 'azaza\n \t\t\t\t \\ test '
    with open(filename, 'w') as f:
        f.write(file_content)

    function_test(
        lambda: cat(stream(), filename),
        expected_code='zero',
        expected_out=file_content,
        expected_err=''
    )

    function_test(
        lambda: cat(stream('ignore it'), filename),
        expected_code='zero',
        expected_out=file_content,
        expected_err=''
    )

    function_test(
        lambda: cat(stream(), 'unknown_file.hehe'),
        expected_code='non zero',
        expected_out='',
        expected_err='file unknown_file.hehe does not found\n'
    )

    function_test(
        lambda: cat(stream(), '/tmp'),
        expected_code='non zero',
        expected_out='',
        expected_err='/tmp is not file\n'
    )


def test_cat_two_files():
    filename_1 = get_temp_file('file_1')
    filename_2 = get_temp_file('file_2')

    function_test(
        lambda: cat(stream(), filename_1, filename_2),
        expected_code='zero',
        expected_out='file_1file_2',
        expected_err=''
    )


def test_cat_only_input_stream():
    text = 'test\t text\t\n'
    function_test(
        lambda: cat(stream(text)),
        expected_code='zero',
        expected_out=text,
        expected_err=''
    )


def test_echo():
    values = ['1', '2', '3', 'hehe', '1337', '14', '42']
    text = ' '.join(values) + '\n'

    function_test(
        lambda: echo(stream(), *values),
        expected_code='zero',
        expected_out=text,
        expected_err=''
    )

    function_test(
        lambda: echo(stream('        '.join(values))),
        expected_code='zero',
        expected_out='\n',
        expected_err=''
    )

    function_test(
        lambda: echo(stream('ignore it'), text),
        expected_code='zero',
        expected_out=text + '\n',
        expected_err=''
    )

    function_test(
        lambda: echo(stream('ignore it'), *values),
        expected_code='zero',
        expected_out=text,
        expected_err=''
    )


def test_wc():
    function_test(
        lambda: wc(stream(), get_temp_file()),
        expected_code='zero',
        expected_err=''
    )

    function_test(
        lambda: wc(cat(stream(), get_temp_file())[1]),
        expected_code='zero',
        expected_err=''
    )

    filename = get_temp_file('test\n\n\n\n123\t\t\t0123')
    code, out, err = wc(cat(stream(), filename)[1])
    text = out.getvalue().decode()
    text = text[:len(text) - 1]  # remove last '\n'

    function_test(
        lambda: wc(stream(), filename),
        expected_code='zero',
        expected_out=text + f'{filename}\n',
        expected_err=''
    )


def test_wc_newline():
    function_test(
        lambda: wc(stream('123\n')),
        expected_code='zero',
        expected_out='\t1\t1\t4\t\n',
        expected_err=''
    )


def test_wc_values():
    def test_value(file_content, expected_out):
        filename = get_temp_file(file_content)
        function_test(
            lambda: wc(stream(), filename),
            expected_code='zero',
            expected_out=f'{expected_out}\t{filename}\n',
            expected_err=''
        )

    test_value(None, '\t0\t0\t0')
    test_value('123', '\t0\t1\t3')
    test_value('123\n', '\t1\t1\t4')
    test_value('\n\n\n\n\n\n\n', '\t7\t0\t7')


def test_pwd():
    function_test(
        lambda: pwd(stream()),
        expected_code='zero',
        expected_err=''
    )
