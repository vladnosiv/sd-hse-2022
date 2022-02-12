import os
from substitute import Substitute


sub = Substitute()


def test_deref__export_empty_value__nothing_changed():
	assert sub.deref('a=') == 'a='


def test_deref__export_empty_string__empty_value():
	sub.deref('a=""')
	assert sub.deref('$a') == ''

	sub.deref("b=''")
	assert sub.deref('$b') == ''


def test_deref__export_word__word():
	sub.deref('a=qwerty')
	assert sub.deref('$a') == 'qwerty'


def test_deref__export_string__quotes_removed():
	sub.deref('a="qwerty"')
	assert sub.deref('$a') == 'qwerty'

	sub.deref("b='qwerty'")
	assert sub.deref('$b') == 'qwerty'


def test_deref__get_path_value__path_value():
	assert sub.deref('$PATH') == os.environ['PATH']


def test_deref__word__variables_replaced():
	sub.deref('a=3.')
	sub.deref('b=22')
	assert sub.deref('$a$b') == '3.22'


def test_deref__weak_quote__variabled_replaced():
	sub.deref('a=3.')
	sub.deref('b=22')
	assert sub.deref('"$a$b"') == '"3.22"'


def test_deref__strong_quote__nothing_changed():
	sub.deref('a=3.')
	sub.deref('b=22')
	assert sub.deref("'$a$b'") == "'$a$b'"
