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
