import mock
import re
from unittest import TestCase

from kwonly_args import first_kwonly_arg, KWONLY_REQUIRED


def test_log(*args, **kwargs):
    pass


class TestErrors(TestCase):
    def test_trying_to_decorate_a_function_without_default_args(self):
        def func(a, b):
            pass

        self.assertRaisesRegexp(
            TypeError,
            re.escape("You can't use @first_kwonly_arg on a function that doesn't have default arguments!"),
            first_kwonly_arg('b'),
            func,
        )

    def test_first_kwonly_arg_name_is_invalid(self):
        def func(a, b=None):
            pass

        self.assertRaisesRegexp(ValueError, re.escape("doesn't have an argument with the specified first_kwonly_arg"),
                                first_kwonly_arg('invalid'), func)

    def test_first_kwonly_arg_name_isnt_a_default_arg(self):
        def func(a, b=None):
            pass

        self.assertRaisesRegexp(ValueError, re.escape("The specified first_kwonly_arg='a' must have a default value!"),
                                first_kwonly_arg('a'), func)

    def test_missing_required_arg(self):
        @first_kwonly_arg('c')
        def func(a, c=None):
            pass

        self.assertRaisesRegexp(
            TypeError,
            r"missing 1 required positional argument|takes at least 1 argument \(0 given\)",
            func,
        )

    def test_missing_required_kwarg(self):
        @first_kwonly_arg('a')
        def func(a=KWONLY_REQUIRED):
            pass

        self.assertRaisesRegexp(TypeError, re.escape("func() missing 1 keyword-only argument(s): a"), func)

    def test_missing_required_kwargs(self):
        @first_kwonly_arg('a')
        def func(a=KWONLY_REQUIRED, b=KWONLY_REQUIRED):
            pass

        self.assertRaisesRegexp(TypeError, re.escape("func() missing 2 keyword-only argument(s): a, b"), func)
        self.assertRaisesRegexp(TypeError, re.escape("func() missing 1 keyword-only argument(s): b"), func, a=0)
        self.assertRaisesRegexp(TypeError, re.escape("func() missing 1 keyword-only argument(s): a"), func, b=0)


@first_kwonly_arg('d1')
def func_defaults_only(d0='d0', d1='d1', d2='d2'):
    test_log(d0=d0, d1=d1, d2=d2)


@mock.patch(__name__ + '.test_log')
class TestDefaultsOnly(TestCase):
    def test_d0_can_be_passed_as_positional_arg(self, mock_test_log):
        func_defaults_only(0)

        mock_test_log.assert_called_once_with(d0=0, d1='d1', d2='d2')

    def test_too_many_positional_args(self, mock_test_log):
        self.assertRaises(TypeError, func_defaults_only, 0, 1)

        self.assertFalse(mock_test_log.called)


@first_kwonly_arg('d1')
def func_args_and_defaults(a0, a1, d0='d0', d1='d1', d2='d2'):
    test_log(a0=a0, a1=a1, d0=d0, d1=d1, d2=d2)


@mock.patch(__name__ + '.test_log')
class TestArgsAndDefaults(TestCase):
    def test_missing_arg(self, mock_test_log):
        self.assertRaises(TypeError, func_args_and_defaults)
        self.assertRaises(TypeError, func_args_and_defaults, 0)
        self.assertFalse(mock_test_log.called)

    def test_passing_only_required_args_as_positional_args(self, mock_test_log):
        func_args_and_defaults(0, 1, d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='d1', d2='my_d2')

    def test_passing_only_required_args_as_positional_and_keyword_args(self, mock_test_log):
        func_args_and_defaults(0, a1=1, d1='my_d1')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='my_d1', d2='d2')

    def test_passing_only_required_args_as_keyword_args(self, mock_test_log):
        func_args_and_defaults(a0=0, a1=1, d1='my_d1', d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='my_d1', d2='my_d2')

    def test_d0_can_be_passed_as_positional_arg(self, mock_test_log):
        func_args_and_defaults(0, 1, 2, d1='my_d1')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0=2, d1='my_d1', d2='d2')

    def test_too_many_positional_args(self, mock_test_log):
        self.assertRaises(TypeError, func_args_and_defaults, 0, 1, 2, 3)


@first_kwonly_arg('d1')
def func_defaults_and_varargs(d0='d0', d1='d1', d2='d2', *args):
    test_log(d0=d0, d1=d1, d2=d2, args=args)


@mock.patch(__name__ + '.test_log')
class TestDefaultsAndVarargs(TestCase):
    def test_passing_no_arg(self, mock_test_log):
        func_defaults_and_varargs()
        mock_test_log.assert_called_once_with(d0='d0', d1='d1', d2='d2', args=())

    def test_can_pass_any_number_of_positional_args_as_varargs(self, mock_test_log):
        func_defaults_and_varargs(0, 1, 2, 3, 4, 5, 6, 7, 8, d2='my_d2')
        mock_test_log.assert_called_once_with(d0=0, d1='d1', d2='my_d2', args=(1, 2, 3, 4, 5, 6, 7, 8))


@first_kwonly_arg('d1')
def func_args_and_defaults_and_varargs(a0, a1, d0='d0', d1='d1', d2='d2', *args):
    test_log(a0=a0, a1=a1, d0=d0, d1=d1, d2=d2, args=args)


@mock.patch(__name__ + '.test_log')
class TestArgsAndDefaultsAndVarargs(TestCase):
    def test_missing_arg(self, mock_test_log):
        self.assertRaises(TypeError, func_args_and_defaults_and_varargs)
        self.assertRaises(TypeError, func_args_and_defaults_and_varargs, 0)
        self.assertFalse(mock_test_log.called)

    def test_passing_only_required_args_as_positional_args(self, mock_test_log):
        func_args_and_defaults_and_varargs(0, 1, d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='d1', d2='my_d2', args=())

    def test_passing_only_required_args_as_positional_and_keyword_args(self, mock_test_log):
        func_args_and_defaults_and_varargs(0, a1=1, d1='my_d1')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='my_d1', d2='d2', args=())

    def test_passing_only_required_args_as_keyword_args(self, mock_test_log):
        func_args_and_defaults_and_varargs(a0=0, a1=1, d1='my_d1', d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0='d0', d1='my_d1', d2='my_d2', args=())

    def test_d0_can_be_passed_as_positional_arg(self, mock_test_log):
        func_args_and_defaults_and_varargs(0, 1, 2, d1='my_d1')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0=2, d1='my_d1', d2='d2', args=())

    def test_can_pass_any_number_of_positional_args_as_varargs(self, mock_test_log):
        func_args_and_defaults_and_varargs(0, 1, 2, 3, 4, 5, 6, 7, 8, d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0=2, d1='d1', d2='my_d2', args=(3, 4, 5, 6, 7, 8))
