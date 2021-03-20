
from lark import (
    Lark,
    Transformer as BaseTransformer,
    v_args,
    Tree
)

from unit import Unit, Widget

GRAMMAR_FILE = 'aewl/grammar.lark'

class Transformer(BaseTransformer):
    @v_args(inline=True)
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    array = list
    number = v_args(inline=True)(float)


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
        if t.data in ('widget_def', 'display_def'):
            name, inherits = t.children[:2]
            widget = unit.add_widget(
                str(name), inherits, is_display=(t.data == 'display_def'))

            parse_widget(widget, t.children[2])
        elif t.data == 'variable_def':
            parse_variable(unit, t)
        else:
            raise Exception('Unexpected %s' % t.data)

    return tree


if __name__ == '__main__':

    with open('example') as fp:
        print(parse(fp.read(), '').pretty())
