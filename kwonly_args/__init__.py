# -*- coding: utf-8 -*-

import functools
import inspect


__all__ = ['first_kwonly_arg', 'KWONLY_REQUIRED']

# version_info[0]: Increase in case of large milestones/releases.
# version_info[1]: Increase this and zero out version_info[2] if you have explicitly modified
#                  a previously existing behavior/interface.
#                  If the behavior of an existing feature changes as a result of a bugfix
#                  and the new (bugfixed) behavior is that meets the expectations of the
#                  previous interface documentation then you shouldn't increase this, in that
#                  case increase only version_info[2].
# version_info[2]: Increase in case of bugfixes. Also use this if you added new features
#                  without modifying the behavior of the previously existing ones.
version_info = (1, 0, 3)
__version__ = '.'.join(str(n) for n in version_info)
__author__ = 'István Pásztor'
__license__ = 'MIT'


KWONLY_REQUIRED = ('KWONLY_REQUIRED',)


def first_kwonly_arg(name):
    """ Emulates keyword-only arguments under python2. Works with both python2 and python3.
    With this decorator you can convert all or some of the default arguments of your function
    into kwonly arguments. Use ``KWONLY_REQUIRED`` as the default value of required kwonly args.

    :param name: The name of the first default argument to be treated as a keyword-only argument. This default
    argument along with all default arguments that follow this one will be treated as keyword only arguments.

        >>> # this decoration converts the ``d1`` and ``d2`` default args into kwonly args
        >>> @first_kwonly_arg('d1')
        >>> def func(a0, a1, d0='d0', d1='d1', d2='d2', *args, **kwargs):
        >>>     print(a0, a1, d0, d1, d2, args, kwargs)
        >>>
        >>> func(0, 1, 2, 3, 4)
        0 1 2 d1 d2 (3, 4) {}
        >>>
        >>> func(0, 1, 2, 3, 4, d2='my_param')
        0 1 2 d1 my_param (3, 4) {}
    """
    def decorate(wrapped):
        arg_names, varargs, _, defaults = inspect.getargspec(wrapped)
        if not defaults:
            raise TypeError("You can't use @first_kwonly_arg on a function that doesn't have default arguments!")

        try:
            first_kwonly_index = arg_names.index(name)
        except ValueError:
            raise ValueError("{}() doesn't have an argument with the specified first_kwonly_arg={!r} name"
                             .format(getattr(wrapped, '__name__', '?'), name))

        first_default_index = len(arg_names) - len(defaults)
        if first_kwonly_index < first_default_index:
            raise ValueError("The specified first_kwonly_arg={!r} must have a default value!".format(name))

        kwonly_defaults = defaults[-(len(arg_names)-first_kwonly_index):]
        kwonly_args = tuple(zip(arg_names[first_kwonly_index:], kwonly_defaults))
        required_kwonly_args = frozenset(arg for arg, default in kwonly_args if default is KWONLY_REQUIRED)

        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            if required_kwonly_args:
                missing_kwonly_args = required_kwonly_args.difference(kwargs.keys())
                if missing_kwonly_args:
                    raise TypeError("{func_name}() missing {count} keyword-only argument(s): {args}".format(
                                    func_name=getattr(wrapper, '__name__', '?'),
                                    count=len(missing_kwonly_args),
                                    args=', '.join(sorted(missing_kwonly_args))))
            if len(args) > first_kwonly_index:
                if varargs is None:
                    raise TypeError(
                        "{func_name}() takes {exactly_or_at_least} {expected_args} arguments ({actual_args} given)"
                        .format(func_name=getattr(wrapper, '__name__', '?'),
                                exactly_or_at_least='exactly' if varargs is None else 'at least',
                                expected_args=first_kwonly_index, actual_args=len(args)))
                kwonly_args_from_kwargs = tuple(kwargs.pop(arg, default) for arg, default in kwonly_args)
                args = args[:first_kwonly_index] + kwonly_args_from_kwargs + args[first_kwonly_index:]

            return wrapped(*args, **kwargs)

        return wrapper
    return decorate
