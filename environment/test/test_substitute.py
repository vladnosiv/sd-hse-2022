import os
from environment import Substitute


sub = Substitute()


def test_deref__get_path_value__path_value():
    assert sub.deref('$PATH') == os.environ['PATH']


def test_deref__strong_quote__nothing_changed():
    sub.deref('a=3.')
    sub.deref('b=22')
    assert sub.deref("'$a$b'") == "'$a$b'"
