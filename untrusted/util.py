import collections.abc
import untrusted


def _wrap_arg(arg):
    if isinstance(arg, untrusted.string):
        return arg.value
    elif isinstance(arg, str):
        return arg
    elif isinstance(arg, collections.abc.Mapping):
        return _wrap_kwargs(**arg)
    elif hasattr(arg, "__iter__"):
        return map(lambda x: _wrap_arg(x), arg)
    else:
        return arg


def _wrap_args(*args):
    return map(_wrap_arg, args)


def _wrap_kwargs(**kwargs):
    _kwargs = dict()

    for key, value in kwargs.items():
        _kwargs[key] = _wrap_arg(value)

    return _kwargs



def _wrapped_method(self, name):
    '''Get a method, normalising untrusted.string and str arguments to str,
       and str results to untrusted.string, and complicated results to
       an appropriate type.'''
    if name in self._safe_methods:
        return _safe_method_wrapper(self, getattr(self.value, name))
    elif name in self._simple_wrapped_methods:
        return _simple_method_wrapper(self, getattr(self.value, name))
    elif name in self._complex_wrapped_methods:
        result_wrapper = self._complex_wrapped_methods.get(name)
        return _complex_method_wrapper(self, result_wrapper, getattr(self.value, name))
    else:
        raise TypeError("attribute %s not supported by %s.%s" % (repr(name), type(self).__module__, type(self).__name__))


def _safe_method_wrapper(self, fn):
    '''For a method returning a safe value and taking any number of
       arguments, optionally accepting untrusted.string types in place of
       `str` arguments, return the result as normal.'''

    def wrapper(*args, **kwargs):
        _args, _kwargs = _wrap_args(*args), _wrap_kwargs(**kwargs)
        result = fn(*_args, **_kwargs)
        assert not isinstance(result, str)
        return result

    return wrapper


def _simple_method_wrapper(self, fn):
    '''For a method returning a string value and taking any number of
       arguments, optionally accepting untrusted.string types in place of
       `str` arguments, return the result as an `untrusted.string`.'''

    def wrapper(*args, **kwargs):
        _args, _kwargs = _wrap_args(*args), _wrap_kwargs(**kwargs)
        result = fn(*_args, **_kwargs)
        if result is None: return None
        return self.__class__(result)

    return wrapper


def _complex_method_wrapper(self, result_wrapper, fn):
    '''For a method returning any type of value, and taking any number of
       arguments, optionally accepting untrusted.string types in place of
       `str` arguments, return the result as an appropriate
        `untrusted.*` type.'''

    def wrapper(*args, **kwargs):
        _args, _kwargs = _wrap_args(*args), _wrap_kwargs(**kwargs)
        result = fn(*_args, **_kwargs)
        return result_wrapper(result)

    return wrapper




# "For custom classes, implicit invocations of special methods are only
# guaranteed to work correctly if defined on an object’s type, not in the
# object’s instance dictionary."

# https://docs.python.org/3.4/reference/datamodel.html#special-method-lookup

def _bindPassthroughMethod(methodName):
    """(Private implementation detail). Magic methods, like __eq__, aren't
    normally accessed through __getattr__ by Python when overloading an
    operator. This function returns a stub wrapper method for the dict of a
    dynamically constructed class. It's useful only if there is a __getattr__
    implementation on the class that provides an alternate implementation."""

    assert methodName.startswith("__"), "use this for magic methods only!"

    def passthroughMethod(self, *args, **kwargs):
        return self.__getattr__(methodName)(*args, **kwargs)

    return passthroughMethod


def _createMagicPassthroughBindings(names):
    result = dict()

    for name in names:
        name = "__%s__" % name
        result[name] = _bindPassthroughMethod(name)

    print(result)
    return result



