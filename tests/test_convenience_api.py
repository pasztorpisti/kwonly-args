import mock
from unittest import TestCase

from kwonly_args import first_kwonly_arg, FIRST_DEFAULT_ARG, kwonly_defaults


def test_log(*args, **kwargs):
    pass


def func_args_and_defaults_and_varargs(a0, a1, d0='d0', d1='d1', d2='d2', *args):
    test_log(a0=a0, a1=a1, d0=d0, d1=d1, d2=d2, args=args)


@mock.patch(__name__ + '.test_log')
class TestFirstDefaultArgParam(TestCase):
    """ Tests passing the FIRST_DEFAULT_ARG constant to the @first_kwonly_arg() decorator. """
    def test_first_default_arg(self, mock_test_log):
        decorated = first_kwonly_arg(FIRST_DEFAULT_ARG)(func_args_and_defaults_and_varargs)
        decorated(0, 1, 2, 3)
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='d1', d2='d2', args=(2, 3))

    def test_kwonly_defaults_decorator(self, mock_test_log):
        decorated = kwonly_defaults(func_args_and_defaults_and_varargs)
        decorated(0, 1, 2, 3)
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='d1', d2='d2', args=(2, 3))
