

class A:
    def __new__(cls, *args, **kwargs):
        return B.__new__(B, *args, **kwargs)


class B:
    pass


print(A())