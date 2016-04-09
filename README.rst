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


.. contents::


-----
Usage
-----


Installation
------------

.. code-block:: sh

    pip install kwonly-args

Alternatively you can download the zipped library from https://pypi.python.org/pypi/kwonly-args


Quick-starter
-------------

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

    from kwonly_args import first_kwonly_arg


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


If you want to turn all default arguments into keyword-only arguments then the following convenience API may be useful
and more convenient:

.. code-block:: python

    from kwonly_args import first_kwonly_arg, FIRST_DEFAULT_ARG, kwonly_defaults


    # The FIRST_DEFAULT_ARG constant automatically selects the first default
    # argument (default0) so it turns all default arguments into keyword-only.
    @first_kwonly_arg(FIRST_DEFAULT_ARG)
    def func(arg0, arg1, default0='d0', default1='d1', *args):
        ...


    # As an equivalent shortcut you can use @kwonly_defaults.
    @kwonly_defaults
    def func(arg0, arg1, default0='d0', default1='d1', *args):
        ...


Why use keyword-only arguments?
-------------------------------

You may have an understanding of this topic. If not then read along.
Using keyword-only arguments provides the following benefits:


Code readability
................

It can make code that calls your function more readable. This is especially true if you have several functions with
long argument lists like some of the python standard library APIs. For example ``subprocess.Popen()`` has more than
10 arguments. ``subprocess.Popen()`` is a legacy function from python2 (so it couldn't make use of keyword-only
arguments despite being a very good candidate for that) but some newer python3 APIs make use of keyword-only
arguments with a good reason. For example the python3 ``subprocess.run()`` has about 10 arguments but only
the first ``argv`` argument can be passed as positional, the rest are keyword-only.

.. code-block:: python

    def draw_circle(x, y, radius, filled=False):
        ...

    def draw_ellipse(x, y, radius_x, radius_y, filled=False):
        ...

    # 1. calling without using keyword arguments:
    draw_circle(100, 200, 50, True)
    draw_ellipse(200, 100, 100, 50)

    # 2. calling using keyword arguments:
    draw_circle(x=100, y=200, radius=50, filled=True)
    draw_ellipse(x=200, y=100, radius_x=100, radius_y=50)

Without keyword-only arguments users of your function will be able to use both of the above conventions. If you
employ keyword-only arguments then they can use only #2. In case of a simple function like my ``draw_circle()`` it
may not seem reasonable enough to force keyword-only arguments. But imagine what happens if you start having many
similar functions like ``draw_ellpise()``, ``draw_rectangle()``, etc.. and you have to read code that calls these
without keyword arguments with a bunch of listed numbers and bools mixed together as their input... The above
example in section #1 is relatively lightweight compared to what it can look in real life.

When a function has more than 3-4 arguments (like ``subprocess.Popen()``) I think it is a very good practice to
allow at most the first few (or none of the) arguments to be passed as positional ones and make the rest kw-only
(like the standard python3 ``subprocess.run()``).
It isn't a problem if a function has a lot of parameters (especially default ones) as long as the code that calls
the function remains readable by using keyword argument passing and you can enforce/guarantee that by making the
most of the arguments keyword-only:

.. code-block:: python

    import subprocess

    argv = ['ls', '-l']

    # BAD! I think I don't really have to explain why...
    p = subprocess.Popen(argv, -1, None, subprocess.PIPE, subprocess.PIPE,
                         subprocess.STDOUT, None, True, True)

    # GOOD! And this has the same behavior as the previous call.
    # I think it is well worth enforcing this form with keyword-only args.
    p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)

    # If the number of passed arguments exceeds my threshold
    # I switch to the following format for readability:
    p = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )


Easier maintenance and refactorization
......................................

Keyword-only args have an extremely useful property: you can declare them in any order in your function signature and
the code that calls your function can also pass them in any order.
Later you can change the order of declaration of your keyword-only arguments for cosmetic and readability reasons
without affecting behavior and without having to refactor code that calls this function. This comes in handy not only
in case of code cosmetics but also makes it easier to add new keyword-only args and to remove old ones if necessary.
Let's review these scenarios with code examples.

Imagine a scenario where you have a ``draw_circle(x, y, radius, outline_color=black, filled=False, fill_color=None)``
function. It already looks bad enough without keyword-only args. Let's imagine that someone asks you to add an
`outline_width` argument. Since all parameters can be passed as positional arguments you have to keep backward
compatibility and you have to append this argument to the end of the current arg list with a default value. This
introduces another ugly thing: the arguments that belong to the outline aren't adjacent. There will be two unrelated
args between ``outline_color`` and the newly added ``outline_width``. If these args were keyword-only arguments then
the arbitrary argument order would allow you to insert the new ``outline_width`` arg right after ``outline_color``.

Another typical and similar scenario is having a function that makes use of 2 or more other functions. For this reason
it receives input args and passes them through to the two other functions. Let's say you start out with something like
this at the beginning of your project:

.. code-block:: python

    # lower level workhorse functions used by the higher level ``my_func()``
    def workhorse1(wh1_1, wh1_2):
        ...

    def workhorse2(wh2_1, wh2_2):
        ...

    # And your function looks like this
    def my_func(wh1_1, wh2_1, wh2_2):
        # TODO: perhaps manipulate the input args...
        workhorse1(wh1_1, 8)
        workhorse2(wh2_1, wh2_2)


Then for some reason someone introduces a new ``wh1_3`` parameter for ``workhorse1()`` and you have to pass it through
your higher level ``my_func()``. It will look like this:

.. code-block:: python

    # One arg for wh1, then two args for wh2 and then another arg for wh1... Nice.
    def my_func(wh1_1, wh2_1, wh2_2, wh1_3):
        # TODO: perhaps manipulate the input args...
        workhorse1(wh1_1, 8)
        workhorse2(wh2_1, wh2_2)


In python you can avoid such scenarios by passing such arguments in ``**kwargs`` or in separate dictionaries but it
often makes the code less explicit and readable:

.. code-block:: python

    # It is more difficult to find out what's going on with ``*args``
    # and ``**kwargs`` then with explicitly named arguments.
    def my_func(**kwargs):
        # Let the workhorses to cherry pick the parameters they
        # need and ignore the rest that they don't need.
        workhorse1(**kwargs)
        workhorse2(**kwargs)


You can also use two separate dictionaries or data objects to pass the arguments to the workhorses. This technique
is better than keyword only argument passing when the workhorses have a lot of parameters and/or you have to pass
the arguments deeply through several calls but this solution is an an overkill in many simpler situations where the
number of parameters isn't too high and there is no deep arg passing:

.. code-block:: python

    def my_func(wh1_args, wh2_args):
        # TODO: perhaps manipulate the input args...
        workhorse1(wh1_args)
        workhorse2(wh2_args)


With keyword-only arguments the above problems don't exist. The new `wh1_3` argument can be placed anywhere in the
keyword-only argument part of the argument list (e.g.: after ``wh1_1``) without affecting the rest of the code that
already calls this functions with other keyword-only args (given that they don't want to use the newly added arg).


--------------
Implementation
--------------


Python 2 function signature anatomy
-----------------------------------

A python2 function signature consists of the following optional parts. Any optional parts that are present in
a function signature appear in the listed order:

1.  Positional arguments

    1.  Required arguments (positional arguments without default value)
    2.  Default arguments (positional arguments with default value)
    3.  **Keyword-only arguments (non-standard, emulated/provided by this library)**

2.  VarArgs (``*args``)
3.  VarKWArgs (``**kwargs``)


As you see in standard python2 your positional argument list consists of zero or more required arguments followed by
zero or more default arguments. This library can turn the last N default arguments (all/some of them) into keyword-only
arguments. With the help of this library you can now split the positional argument list of your python2 function
signatures into 3 parts instead of the standard 2.

In python3 the keyword-only arguments reside between VarArgs and VarKWArgs but in python2 you can't put anything
between those (it would be a syntax error) so your best bet to emulate keyword-only arguments is turning some of your
positional arguments into keyword-only args.


Emulated keyword-only args VS static analyzers
..............................................

As discussed previously unfortunately we can declare our emulated python2 keyword-only arguments only before the
VarArgs (``*args``) of the function. This means that our signature can have positional arguments not only before our
keyword-only args, but also after them (because VarArgs are positional). This may lead to false-positive
warnings/errors with static analyzers in the following case:

If you have a function with both keyword-only arguments and VarArgs then static analyzers may treat some
of the calls to this function suspicious (resulting in a false positive warning/error).

.. code-block::

    @first_kwonly_arg('ko0')
    def func(a0, d0=-1, ko0=-1, ko1=-1, *args):
        ...


    # No problem: a0=0
    func(0)

    # No problem: a0=0, d0=1
    func(0, 1)

    # No problem: a0=0 d0=1 args=(2,)
    func(0, 1, 2)

    # The static analyzer will probably treat this as an error. It thinks that
    # you pass both the positional argument 2 and ko0=3 to the ko0 arg of the
    # function because it can't track down the magic done by the @first_kwonly_arg
    # decorator and binds the passed parameters to the function args using standard
    # python2 rules. If func() didn't have our @first_kwonly_arg decorator then
    # this function call would probably cause an error like:
    # TypeError: func() got multiple values for argument 'ko0'
    #
    # However what actually happens as a result of the magic done by the
    # decorator is: a0=0 d0=1 ko0=3 ko1=-1 args=(2,)
    # The decorator ensures that positional parameters passed by function calls
    # are bound only to positional non-keyword-only arguments and the VarArgs
    # of the function.
    func(0, 1, 2, ko0=3)

    # No problem despite the fact that the static analyzer probably assumes
    # something different than what actually happens. According to standard
    # python2 arg binding rules the static analyzer probably thinks that:
    # a0=0 d0=1 ko0=2 ko1=3 args=()
    #
    # However the actual outcome caused by our decorator is:
    # a0=0 d0=1 ko0=-1 ko1=3 args=(2,)
    func(0, 1, 2, ko1=3)


Despite the above issue a decorator like this can still be very useful. The reason for this is that for me it happens
quite rarely that in a function I need both keyword-only arguments and VarArgs. I need VarArgs quite rarely in general
while keyword-only arguments come in handy quite often. If this is the same for you then go on using this decorator in
your python2 projects and in the rare cases where you need both keyword-only arguments and VarArgs use one of the
following workarounds to aid this issue:

- Don't use a static analyzer. (Well, this was only a joke. :-D)
- In your static analyzer tool or service ignore the individual instances of these false positive warnings.
- Use `Poor man's python2 keyword-only arguments`_ with these problematic cases instead of decorating them and use the
  decorator only with the rest (probably the majority) of the functions that don't have VarArgs.


Why does this "library" exist?
------------------------------

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

.. _decorator_source: https://github.com/pasztorpisti/kwonly-args/blob/fa4cb674c9235a68642687deb272a25e257f49df/kwonly_args/__init__.py#L70-L111

__ decorator_source_


Poor man's python2 keyword-only arguments
-----------------------------------------

I really like the benefits brought by keyword-only arguments. Long ago before extensively working with python I've
already forged some coding-convention rules that have similar advantages (unordered arguments, specifying arg names
while calling the function for readability) in other languages (e.g.: C/C++). Before thinking about using a python2
solution like the one provided by this library I've used a "manually implemented poor man's python2 keyword-only args"
solution like this:

.. code-block:: python

    def func(arg0, arg1, default0='d0', default1='d1', **kwargs):
        # Keyword-only arg with a default value:
        optional_kwonly0 = kwargs.pop('kwonly0', 'ko0')
        # Required keyword-only arg:
        required_kwonly1 = kwargs.pop('kwonly1')

        # Checking whether the caller has passed an unexpected keyword argument.
        # Sometimes passing an unexpected keyword argument is simply the result
        # of a typo in the name of an expected arg. E.g.: kwnly0 instead of kwonly0
        check_no_kwargs_left(func, kwargs)

        # ... the rest of the function body


    # utility function far away somewhere in a central place...
    def check_no_kwargs_left(func_or_func_name, kwargs):
        if not kwargs:
            return
        func_name = func_or_func_name.__name__ if callable(func_or_func_name) else func_or_func_name
        arg_names = ', '.join(repr(k) for k in sorted(kwargs.keys()))
        raise TypeError('{func_name}() got unexpected keyword argument(s): {arg_names}'.format(
                        func_name=func_name, arg_names=arg_names))


While I think the above solution if fairly good it still requires checking the function body too in order to see the
full signature and sometimes people may forget to check for leftover kwargs after popping the kwonly args.
