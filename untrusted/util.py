

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


