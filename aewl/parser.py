
from lark import (
    Lark,
    Transformer as BaseTransformer,
    v_args,
    Tree
)

from .unit import Unit
from .helpers import Percentage
from .widgets import Widget, Display, Resource

GRAMMAR_FILE = 'aewl/grammar.lark'

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
        elif value.data == 'widget_def':
            name, inherits = value.children[:2]
            widget = scope.make_widget(str(name), inherits)

            parse_widget(widget, value.children[2])

            return widget
        elif value.data == 'variable':
            return scope.get_variable(str(value.children[0]))
        elif value.data == 'property':
            if not isinstance(scope, Widget):
                raise Exception('property can not be defined outside widget')

            return scope.get_property(str(value.children[0]))
    elif isinstance(value, list):
        value = [parse_value(x, scope) for x in value]

    return value

def parse_widget(widget, tree):
    for t in tree.children:
        if t.data == 'variable_def':
            parse_variable(widget, t)
        elif t.data == 'property_def':
            name, value = t.children

            widget.add_property(str(name), parse_value(value, widget))
        else:
            raise Exception('Unexpected %s' % t.data)


def parse_variable(scope, tree):
    scope.add_variable(
        str(tree.children[0]), parse_value(tree.children[1], scope))

def parse(src, name):
    l = Lark.open(GRAMMAR_FILE, parser='lalr', transformer=Transformer())
    tree = l.parse(src)

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
        elif t.data == 'variable_def':
            parse_variable(unit, t)
        else:
            raise Exception('Unexpected %s' % t.data)

    return unit

