===========
kwonly-args
===========


.. image:: https://img.shields.io/travis/pasztorpisti/kwonly-args.svg?style=flat
    :target: https://travis-ci.org/pasztorpisti/kwonly-args
    :alt: build

.. image:: https://img.shields.io/codacy/1a359512094746ae9d39e281cdbc581a/master.svg?style=flat
    :target: https://www.codacy.com/app/pasztorpisti/kwonly-args
    :alt: code quality

.. image:: https://landscape.io/github/pasztorpisti/kwonly-args/master/landscape.svg?style=flat
    :target: https://landscape.io/github/pasztorpisti/kwonly-args/master
    :alt: code health

.. image:: https://img.shields.io/coveralls/pasztorpisti/kwonly-args/master.svg?style=flat
    :target: https://coveralls.io/r/pasztorpisti/kwonly-args?branch=master
    :alt: coverage

.. image:: https://img.shields.io/pypi/v/kwonly-args.svg?style=flat
    :target: https://pypi.python.org/pypi/kwonly-args
    :alt: pypi

.. image:: https://img.shields.io/github/tag/pasztorpisti/kwonly-args.svg?style=flat
    :target: https://github.com/pasztorpisti/kwonly-args
    :alt: github

.. image:: https://img.shields.io/github/license/pasztorpisti/kwonly-args.svg?style=flat
    :target: https://github.com/pasztorpisti/kwonly-args/blob/master/LICENSE.txt
    :alt: license: MIT


This library emulates the python3 keyword-only arguments under python2. The resulting code is python3 compatible.


-----
Usage
-----


Installation
------------

.. code-block:: sh

    pip install kwonly-args

Alternatively you can download the zipped library from https://pypi.python.org/pypi/kwonly-args


Code
----

With this library you can turn some or all of the default arguments of your function into keyword-only arguments.

- Decorate your function with ``kwonly_args.first_kwonly_arg`` and select one of the default arguments of your function
  with the ``name`` parameter of the decorator. The selected argument along with all default arguments on its right
  side will be treated as keyword-only arguments.
- All keyword-only arguments have a default value and they aren't required args by default. You can make a
  keyword-only argument required by using ``kwonly_args.KWONLY_REQUIRED`` as its default value.

Your new-born keyword-only args are no longer treated as positional arguments and varargs still work if your function
has ``*args`` or something like that.

.. code-block:: python

    from kwonly_args import first_kwonly_arg, KWONLY_REQUIRED


    # This turns default1 and default2 into keyword-only arguments.
    # They are no longer handled as positional arguments.
    @first_kwonly_arg('default1')
    def func(arg0, arg1, default0='d0', default1='d1', default2='d2', *args):
        print('arg0={} arg1={} default0={} default1={} default2={} args={}'.format(
              arg0, arg1, default0, default1, default2, args))


    func(0, 1, 2, 3, 4)
    # Output:
    # arg0=0 arg1=1 default0=2 default1=d1 default=d2 args=(3, 4)

    # The default1 and default2 args can be passed only as keyword arguments:
    func(0, 1, 2, 3, 4, default1='kwonly_param')
    # Output:
    # arg0=0 arg1=1 default0=2 default1=kwonly_param default=d2 args=(3, 4)


    # In this example all three args are keyword-only args and default1 is required.
    @first_kwonly_arg('default0')
    def func2(default0='d0', default1=KWONLY_REQUIRED, default2='d2'):
        ...


You can also decorate class methods (including both old and new style classes):

.. code-block:: python

    from kwonly_args import first_kwonly_arg, KWONLY_REQUIRED


    class MyClass:
        # turning d1 and d2 into keyword-only arguments
        @first_kwonly_arg('d1')
        def my_instance_method(self, a0, a1, d0='d0', d1='d1', d2='d2', *args):
            ...

        # You have to apply @first_kwonly_arg before @classmethod!
        @classmethod
        @first_kwonly_arg('d1')
        def my_class_method(cls, a0, a1, d0='d0', d1='d1', d2='d2', *args):
            ...

        # You have to apply @first_kwonly_arg before @staticmethod!
        @staticmethod
        @first_kwonly_arg('d1')
        def my_static_method(a0, a1, d0='d0', d1='d1', d2='d2', *args):
            ...


.. warning::

    This library is compatible with python3 but under python3 you can apply the ``kwonly_args.first_kwonly_arg``
    decorator only to functions that have a python2 compatible signature. E.g.: If your function has python3
    keyword-only arguments then applying this decorator fails (because of the used ``inspect.getargspec()`` function
    doesn't support python2-incompatible signatures).

    This library could circumvent this problem by using ``inspect.getfullargspec()`` under python3 but why would we
    emulate keyword-only arguments in python3 when it is natively available and why whould we apply a python2
    helper library on a piece of code that doesn't even compile under python2? On top of this it would provide
    two different places (before and after the varargs - eumulated and native python3) in your function arg list to
    specify keyword-only arguments - this is just ugly from a design perspective.


--------------
Implementation
--------------


Python 2 function signature anatomy
-----------------------------------

A python2 function argument list consists of the following optional parts. Any optional parts that are present in
a function signature appear in the listed order:

1.  Positional arguments

    1.  Required arguments (positional arguments without default value)
    2.  Default arguments (positional arguments with default value)
    3.  **Keyword-only arguments (this is available only when you use this library)**

2.  VarArgs (``*args``)
3.  VarKWArgs (``**kwargs``)


As you see in standard python2 your positional argument list consists of zero or more required arguments followed by
zero or more default arguments. This library can turn the last N default arguments (all/some of them) into keyword-only
arguments. With the help of this library you can now split the positional argument list of your python2 function
signatures into 3 parts instead of the standard 2.

In python3 the keyword-only arguments reside between VarArgs and VarKWArgs but in python2 you can't put anything
between those (it would be a syntax error) so your best bet to emulate keyword-only arguments is turning some of your
positional arguments into keyword-only args.


Why does this "library" exist?
------------------------------

The world gives birth to new things in every single moment. This is a key driver behind evolution. But anyway, you are
just too naive if you think you can stop code-monkeys with this question. :-D Even a bad reimplementation can give
new insights sometimes but in worst case the author learns some new things and learns to appreciate existing
implementations for hiding the discovered hell/complexity.

I've checked out some other python2 keyword-only argument emulator code snippets and decided to roll my own just for
fun and also for the following reasons:

- Some of those implementations provide you with a decorator with which you have to specify your keyword-only arguments
  with their (usually zero based) index in the arg list of the function. This is error prone, I never liked the
  idea of identifying arguments with indexes. The only minor disadvantage of using arg names instead of arg indexes
  is that using arg names requires direct access to the signature of the *original* wrapped function.
  If there are other decorators between our decorator and the original function then under python2 using names isn't
  really possible (because ``functools.update_wrapper()`` and decorators in general don't have/support the
  ``__wrapped__`` attribute to maintain a chain back to the originally wrapped function).
- Some implementations allow you to pick an arbitrary set of positional arguments by specifying their indexes or names.
  I don't like the idea of promoting arbitrary positional arguments into keyword-only arguments by scattering
  keyword-only args through the remaining positional args. It degrades code readability a lot. This is why I decided
  to keep positional arguments of the same type (required/default/kwonly) together in a well defined slice of the
  positional argument list.
- `The implementation of this solution`__ is brief (~40 lines of logic), simple, and well tested.

.. _decorator_source: https://github.com/pasztorpisti/kwonly-args/blob/master/kwonly_args/__init__.py#L27

__ decorator_source_
