
from typing import Union
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class Ref:
    name: str

@dataclass
class PropertyRef(Ref):
    pass

@dataclass
class MacroRef(Ref):
    pass

class InputOperation:
    def __init__(self, sequence):
        if not (len(sequence) & 1):
            raise Exception('Wrong sequence length')

        self.sequence = sequence

    def resolve(self, ctx):
        v = ctx.prep_val(self.sequence[0])

        for idx in range(1, len(self.sequence)-1, 2):
            op, right = self.sequence[idx:idx+2]
            right = ctx.prep_val(right)

            m_name = {
                '+': '__add__',
                '-': '__sub__',
                '*': '__mul__',
                '/': '__div__',
                '%': '__mod__'
            }[op]

            method = getattr(v, m_name)
            v = method(right)

        return v

class Base:
    def __init__(self, name, inherits=None, properties=None):
        self.name = name
        self.macros = {}

        if inherits is None:
            self.inherits = []
        else:
            self.inherits = inherits

        if properties is None:
            self.properties = {}
        else:
            self.properties = properties

    def _key_transform(self, key):
        return key.lower()

    def __setitem__(self, key, value):
        self.properties[self._key_transform(key)] = value

    def __getitem__(self, key):
        return self.properties[self._key_transform(key)]

    def __delitem__(self, key):
        del self.properties[self._key_transform(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self, **kwargs):
        kwargs.setdefault('name', self.name)
        kwargs.setdefault('properties', self.properties)

        if self.inherits is not []:
            kwargs.setdefault('inherits', self.inherits)

        return self.__class__(**kwargs)

class Widget(Base): pass
class Display(Base): pass
class Resource(Base): pass