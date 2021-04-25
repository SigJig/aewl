
import sys

from collections import deque
from functools import cached_property
from armaconfig.config import Config

from .models import Model, Alias, DisplayModel, ResourceModel
from .unit import Unit
from .types import (
    Widget,
    Display,
    Resource,
    Base as TypeBase,
    MacroRef,
    PropertyRef,
    InputOperation
)
from .utils import dictmerge

class Context:
    def __init__(self, obj, parent=None, **kwargs):
        self.obj = obj
        self.parent = parent
        self.export = Config(
            self.obj.name, parent=kwargs.get(
                'parent_export', getattr(self.parent, 'export', None)))

        self.cache = {}
        self.children = []

        if not isinstance(self.obj, Unit):
            self._inheritance, self._models = (
                self._resolve_inheritance(self.obj.inherits))
        else:
            self._inheritance, self._models = deque(), deque()

    def __str__(self):
        return '{}({})'.format(type(self).__name__, self.obj.name)

    def stack(self):
        dq = deque()
        ctx = self

        while ctx is not None:
            dq.appendleft(str(ctx))
            ctx = ctx.parent

        return dq

    def add_child(self, obj, **kwargs):
        ctx = Context(obj, self, **kwargs)
        self.children.append(ctx)

        return ctx

    def macro(self, key):
        try:
            return self.obj.macros[key]
        except KeyError:
            if self.parent is not None:
                return self.parent.macro(key)

            raise

    def default(self, key):
        for m in self._models:
            if key in m.fields:
                return m.fields[key]

        raise KeyError(key)

    def property_global(self, key):
        try:
            return self.property_local(key, use_default=False)
        except KeyError:
            if self.parent is not None:
                return self.parent.property_global(key)

            return None

    def property_local(self, key, use_default=True):
        try:
            return self.obj[key]
        except KeyError:
            for i in self._inheritance:
                try:
                    return i[key]
                except KeyError:
                    pass

            if use_default:
                for m in self._models:
                    if key in m.fields:
                        return m.fields[key]

            raise

    def prep_val(self, val):
        if isinstance(val, MacroRef):
            return self.macro(val.name)
        elif isinstance(val, PropertyRef):
            return self.processed(val.name)
        elif isinstance(val, InputOperation):
            return val.resolve(self)
        elif isinstance(val, list):
            return [self.prep_val(x) for x in val]
        elif isinstance(val, dict):
            return {k: self.prep_val(v) for k, v in val.items()}

        return val

    def prep_export(self, val):
        if isinstance(val, TypeBase):
            return self.prep_export(val.properties)
        elif isinstance(val, dict):
            return {k: self.prep_export(v) for k, v in val.items()}
        elif hasattr(val, 'export'):
            return getattr(val, 'export')()

        return val

    def _process(self, prop):
        value = self.prep_val(
            self.property_local(prop, use_default=True))

        if isinstance(value, dict):
            default = self.default(prop)

            if value is not default:
                value = dictmerge(default.copy(), value)

        for m in self._models:
            meth = getattr(m, prop, None)

            if meth is not None and getattr(meth, 'is_customizer', False):
                if value is not None or not meth.optional:
                    if value is None:
                        value = meth.default

                    result = meth(prop, value)

                    self.cache[prop] = result

                    if getattr(meth, 'export', True):
                        self.export[result.key] = self.prep_export(result.value)

                    return result

        result = Alias(prop, value)
        self.cache[prop] = result
        self.export[result.key] = result.value

        return result

    def processed(self, prop):
        if prop in self.cache:
            return self.cache[prop].value

        return self._process(prop).value

    def process_all(self):
        if isinstance(self.obj, Unit):
            for i in self.obj.widgets.values():
                ctx = self.add_child(i)
                ctx.process_all()

                self.export[i.name] = ctx.export
        else:    
            try:
                keys = set(self.obj.properties.keys())

                for m in self._models:
                    keys |= set(m.fields.keys())

                for k in keys:
                    self.processed(k)
            except Exception as e:
                raise
                #raise Exception('Error in {}\n: {}'.format('\nin '.join(self.stack()), '\n'.join(str(x) for x in sys.exc_info()))) from e

    @cached_property
    def widget_ctx(self):
        if not self.is_widget():
            if self.parent is None:
                return None
            else:
                return self.parent.widget_ctx

        return self

    @cached_property
    def display_ctx(self):
        if not self.is_display():
            if self.parent is None:
                return None
            else:
                return self.parent.display_ctx

        return self

    @cached_property
    def resource_ctx(self):
        if not self.is_resource():
            if self.parent is None:
                return None
            else:
                return self.parent.resource_ctx

        return self

    @cached_property
    def x_ctx(self):
        if not isinstance(self.obj, TypeBase):
            if self.parent is None:
                return None
            else:
                return self.parent.x_ctx

        return self

    def model_method(self, method, *args, **kwargs):
        ctx = self.x_ctx

        for m in ctx._models:
            meth = getattr(m, method, None)

            if meth is not None:
                return meth(*args, **kwargs)

        raise Exception('No method {}'.format(method))

    def is_widget(self) -> bool:
        return isinstance(self.obj, Widget)

    def is_display(self) -> bool:
        return isinstance(self.obj, Display)

    def is_resource(self) -> bool:
        return isinstance(self.obj, Resource)

    def _resolve_inheritance(self, typenames):
        def _make_model(i):
            if isinstance(self.obj, Resource):
                return ResourceModel(i, self)
            elif isinstance(self.obj, Display):
                return DisplayModel(i, self)
            else:
                return Model(i, self)

        inherits = deque()
        models = deque()

        if self.is_display() or self.is_resource():
            models.appendleft(_make_model(None))

        for i in typenames:
            found = self.parent.property_global(i)

            if found is None:
                models.appendleft(_make_model(i))
            elif isinstance(found, dict):
                inherits.appendleft(found)
            elif not isinstance(found, Widget):
                raise Exception('{} is not widget or dict'.format(str(found)))
            else:
                inherits.appendleft(found)

                _i, _m = self._resolve_inheritance(found.inherits)

                inherits.extendleft(_i)
                models.extendleft(_m)

        return inherits, models
