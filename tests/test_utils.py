from unittest import TestCase

from kwonly_args.utils import update_wrapper


class TestUpdateWrapper(TestCase):
    def test_attributes_are_copied(self):
        def dest():
            """ dest doc """

        def src():
            """ src doc """

        src.my_attrib = 'my_attrib'

        self.assertEqual(dest.__name__, 'dest')
        self.assertEqual(dest.__doc__, ' dest doc ')
        self.assertEqual(src.__name__, 'src')
        self.assertEqual(src.__doc__, ' src doc ')
        self.assertEqual(getattr(src, 'my_attrib', None), 'my_attrib')
        self.assertFalse(hasattr(dest, 'my_attrib'))

        result = update_wrapper(dest, src)
        self.assertIs(result, dest)

        self.assertEqual(dest.__name__, 'src')
        self.assertEqual(dest.__doc__, ' src doc ')
        self.assertEqual(src.__name__, 'src')
        self.assertEqual(src.__doc__, ' src doc ')
        self.assertEqual(getattr(dest, 'my_attrib', None), 'my_attrib')
        self.assertEqual(getattr(src, 'my_attrib', None), 'my_attrib')
