import mock
from unittest import TestCase

from kwonly_args import first_kwonly_arg


def test_log(*args, **kwargs):
    pass


class MyClass:
    @first_kwonly_arg('d1')
    def my_instance_method(self, a0, a1, d0='d0', d1='d1', d2='d2', *args):
        test_log(m_self=self, a0=a0, a1=a1, d0=d0, d1=d1, d2=d2, args=args)

    # You have to put @first_kwonly_arg after @classmethod!
    @classmethod
    @first_kwonly_arg('d1')
    def my_class_method(cls, a0, a1, d0='d0', d1='d1', d2='d2', *args):
        test_log(m_cls=cls, a0=a0, a1=a1, d0=d0, d1=d1, d2=d2, args=args)

    # You have to put @first_kwonly_arg after @staticmethod!
    @staticmethod
    @first_kwonly_arg('d1')
    def my_static_method(a0, a1, d0='d0', d1='d1', d2='d2', *args):
        test_log(a0=a0, a1=a1, d0=d0, d1=d1, d2=d2, args=args)


@mock.patch(__name__ + '.test_log')
class TestErrors(TestCase):
    def setUp(self):
        self.instance = MyClass()

    def test_instance_method_missing_required_arg(self, mock_test_log):
        self.assertRaisesRegexp(
            TypeError,
            r"missing 2 required positional argument|takes at least 3 arguments \(1 given\)",
            self.instance.my_instance_method,
        )
        self.assertFalse(mock_test_log.called)

        self.assertRaisesRegexp(
            TypeError,
            r"missing 1 required positional argument|takes at least 3 arguments \(2 given\)",
            self.instance.my_instance_method, 0,
        )
        self.assertFalse(mock_test_log.called)

    def test_class_method_missing_required_arg(self, mock_test_log):
        self.assertRaisesRegexp(
            TypeError,
            r"missing 2 required positional argument|takes at least 3 arguments \(1 given\)",
            MyClass.my_class_method,
        )
        self.assertFalse(mock_test_log.called)

        self.assertRaisesRegexp(
            TypeError,
            r"missing 1 required positional argument|takes at least 3 arguments \(2 given\)",
            MyClass.my_class_method, 0
        )
        self.assertFalse(mock_test_log.called)

    def test_static_method_missing_required_arg(self, mock_test_log):
        self.assertRaisesRegexp(
            TypeError,
            r"missing 2 required positional argument|takes at least 2 arguments \(0 given\)",
            MyClass.my_static_method,
        )
        self.assertFalse(mock_test_log.called)

        self.assertRaisesRegexp(
            TypeError,
            r"missing 1 required positional argument|takes at least 2 arguments \(1 given\)",
            MyClass.my_static_method, 0
        )
        self.assertFalse(mock_test_log.called)


@mock.patch(__name__ + '.test_log')
class TestClassInstance(TestCase):
    def setUp(self):
        self.instance = MyClass()

    def test_instance_method(self, mock_test_log):
        self.instance.my_instance_method(0, 1, 2, 3, 4, d2='my_d2')
        mock_test_log.assert_called_once_with(m_self=self.instance, a0=0, a1=1, d0=2, d1='d1', d2='my_d2', args=(3, 4))

    def test_class_method(self, mock_test_log):
        self.instance.my_class_method(0, 1, 2, 3, 4, d2='my_d2')
        mock_test_log.assert_called_once_with(m_cls=MyClass, a0=0, a1=1, d0=2, d1='d1', d2='my_d2', args=(3, 4))

    def test_static_method(self, mock_test_log):
        self.instance.my_static_method(0, 1, 2, 3, 4, d2='my_d2')
        mock_test_log.assert_called_once_with(a0=0, a1=1, d0=2, d1='d1', d2='my_d2', args=(3, 4))
