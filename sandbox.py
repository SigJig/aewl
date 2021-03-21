
import json
from aewl.parser import parse
from armaconfig import dumps

with open('example') as fp:
    un = parse(fp.read(), fp.name)
    un.process_all()
    
    print(dumps(un.export(), indent=4))