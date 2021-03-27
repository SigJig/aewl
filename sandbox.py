
import json
from aewl.parser import parse
from armaconfig import dump, load

with open('example.aewl') as fp:
    un = parse(fp.read(), fp.name)
    un.process_all()

    with open('tools/configs.githide.hpp') as lp:
        base = load(lp)
    
    with open('out.githide.hpp', 'w') as dp:
        dump(un.export(parent=base), dp, indent=4)