
import json
from aewl import file_to_file
from armaconfig import dump, load

with open('example.aewl') as fp, open('out.githide.hpp', 'w') as dp:
    file_to_file(fp, dp, indent=4)
