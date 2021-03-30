
from pathlib import Path
from lark import (
    Lark,
    Transformer as BaseTransformer,
    v_args,
    Tree
)

from .unit import Unit
from .helpers import Percentage, Operation
from .widgets import Widget, Display, Resource
from .scope import ListScope, DictScope

GRAMMAR_FILE = Path(__file__).parent.absolute().joinpath('data', 'grammar.lark')

class Transformer(BaseTransformer):
    @v_args(inline=True)
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    @v_args(inline=True)
    def inherits(self, *i):
        return [str(x) for x in i]

    def inherits_opt(self, *args, **kwargs):
        return []

    array = list
    number = v_args(inline=True)(float)
    percentage = v_args(inline=True)(Percentage)


def parse_value(value, scope):
    if isinstance(value, Tree):
        if value.data in ('value_expr', 'mul_expr'):
            left, op, right = value.children
            left, right = parse_value(left, scope), parse_value(right, scope)

            m_name = {
                'value_expr': {
                    '+': '__add__',
                    '-': '__sub__'
                },
                'mul_expr': {
                    '*': '__mul__',
                    '/': '__div__',
                    '%': '__mod__'
                }
            }[value.data][op]

            method = getattr(left, m_name)
            
            return method(right)
        elif value.data == 'union_expr':
            left, right = (parse_value(x, scope) for x in value.children)

            if not (isinstance(left, (str, list)) and isinstance(right, (str, list))):
                raise TypeError('union requires two strings')

            return [left, right]
        elif value.data == 'widget_def':
            name, inherits = value.children[:2]
            widget = scope.make_widget(str(name), inherits, parent_widget=scope)

            parse_widget(widget, value.children[2])

            return widget
        elif value.data == 'pod':
            dictscope = DictScope({}, scope)

            for i in value.children[0].children:
                if i.data != 'property_def':
                    raise Exception('supposed to be a property you dense cunt')

                dictscope[str(i.children[0])] = parse_value(i.children[1], dictscope)

            return dictscope
        elif value.data in ('macro', 'property'):
            return scope.get(str(value.children[0]))
    elif isinstance(value, list):
        listscope = ListScope([], scope)

        for x in value:
            listscope.append(parse_value(x, listscope))

        return listscope

    return value

def parse_widget(widget, tree):
    for t in tree.children:
        if t.data == 'macro_def':
            parse_macro(widget, t)
        elif t.data == 'property_def':
            name, value = t.children

            widget.add_property(str(name), parse_value(value, widget))
        else:
            raise Exception('Unexpected %s' % t.data)


def parse_macro(scope, tree):
    scope.add_macro(
        str(tree.children[0]), parse_value(tree.children[1], scope))

def parse(src, name, path_parent=None):
    l = Lark.open(GRAMMAR_FILE, parser='lalr', transformer=Transformer())
    tree = l.parse(src)

    if path_parent is None:
        path_parent = Path.cwd().absolute()

    unit = Unit(name)

    for t in tree.children:
        if t.data in ('widget_def', 'display_def', 'resource_def'):
            name, inherits = t.children[:2]
            type_ = {
                'widget_def': Widget,
                'display_def': Display,
                'resource_def': Resource
            }

            widget = unit.add_widget(
                str(name), inherits, type_=type_[t.data])

            parse_widget(widget, t.children[2])
        elif t.data in ('import_full', 'import_partial', 'import_alias'):
            data, children = t.data, t.children
            partials = []
            
            if data == 'import_full':
                path = children[0]
            elif data == 'import_partial':
                partials, path = children[:-1], children[-1]

                raise NotImplementedError('Partial import not yet supported')
            else:
                path, alias = children
                raise NotImplementedError('Alias import not yet supported')

            if not path.endswith('.aewl'):
                path += '.aewl'

            if not path.startswith('/'):
                path = path_parent.joinpath(path)

            with open(path) as fp:
                unit.add_link(parse(fp.read(), fp.name), partials=partials)

        elif t.data == 'macro_def':
            parse_macro(unit, t)
        else:
            raise Exception('Unexpected %s' % t.data)

    return unit

