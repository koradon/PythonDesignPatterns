class NotSafeSingleton(object):
    """
    This Single ton is not safe in Python 2.7. When some class inherit from this class
    It will not be a singleton!
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NotSafeSingleton, cls).__new__(cls)
        return cls.instance


class Borg(object):
    """
    Borg is also know as monostate. In this pattern, all of the instances are
    different, but they share the same state.
    """
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


class SingletoneDecorator(object):
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


def check_NotSafeSingleton():
    print("Check NotSafeSingleton class")
    singleton = NotSafeSingleton()
    singleton2 = NotSafeSingleton()

    print(singleton is singleton2)

    singleton.some_var = "I'am only var"
    print(singleton2.some_var)

    class Child(NotSafeSingleton):
        pass

    child = Child()
    if child is singleton:
        print("True in Python 3")
    else:
        print("False in Python 2.7")


def check_Borg():
    print("Check Borg class")
    borg = Borg()
    borg2 = Borg()

    print(borg is borg2)

    class Child(Borg):
        pass

    child = Child()

    borg.some_var = "Some var"
    print("child.some_var: {}".format(child.some_var))


def check_SingletonDecorator():
    print("Check SingletonDecorator class")
    class foo: pass
    foo = SingletoneDecorator(foo)
    x=foo()
    y=foo()
    z=foo()
    x.val = 'x'
    y.val = 'y'
    z.val = 'z'

    print(x.val)
    print(y.val)
    print(z.val)

    print(x is y is z)


if __name__ == "__main__":
    check_NotSafeSingleton()
    check_Borg()
    check_SingletonDecorator()
