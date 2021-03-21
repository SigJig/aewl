
import json
from aewl.parser import parse

with open('example') as fp:
    un = parse(fp.read(), fp.name)
    un.process_all()
    
    pass
    #print(json.dumps(, indent=4))