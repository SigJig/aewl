
class _meta(type):
    def __new__(cls, name, bases, attrs):
        for attr in attrs:
            print(attr, getattr(cls, attr, 0))

        return super().__new__(cls, name, bases, attrs)


class A(metaclass=_meta):
    prop = 1

class B(A):
    prop = 2

class C(A):
    prop = 3

class D(C):
    prop = 4