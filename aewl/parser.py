
from lark import (
    Lark,
    Transformer as BaseTransformer,
    v_args
)

from widget import Widget
from unit import Unit

GRAMMAR_FILE = 'aewl/grammar.lark'

class Transformer(BaseTransformer):
    @v_args(inline=True)
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    array = list
    number = v_args(inline=True)(float)

def parse_widget(widget, tree):
    pass

def parse(src, name):
    l = Lark.open(GRAMMAR_FILE, parser='lalr', transformer=Transformer())
    tree = l.parse(src)

    unit = Unit(name)

    for t in tree.children:
        if t.data == 'widget_def':
            widget = unit.add_widget(*t.children[:2])

            parse_widget(widget, t.children)
        elif t.data == 'variable_def':
            pass
        elif t.data == 'display_def':
            pass
        else:
            raise Exception('Unexpected %s' % t.data)

    return tree

if __name__ == '__main__':

    with open('example') as fp:
        print(parse(fp.read()).pretty())