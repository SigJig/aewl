
from lark import Lark

l = Lark.open('aewl/grammar.lark')

with open('example') as fp:
    print(l.parse(fp.read()).pretty())