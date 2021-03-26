
import json
from aewl.parser import parse
from armaconfig import dumps, load

with open('example') as fp:
    un = parse(fp.read(), fp.name)
    un.process_all()

    with open('tools/configs.githide.hpp') as lp:
        base = load(lp)
    
    print(dumps(un.export(parent=base), indent=4))