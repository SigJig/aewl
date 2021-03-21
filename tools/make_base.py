
import io
import requests

from armaconfig import loads
from armaconfig.entry import EOL
from armaconfig.analyse import Parser

FILE_LOCATION = 'https://raw.githubusercontent.com/SigJig/attack-and-defend/master/src/core/gui/common/base.hpp'

def get_styles():
    response = requests.get(FILE_LOCATION)

    if response.status_code != 200:
        raise Exception(response.status_code)

    # with open('a.githide.hpp', 'w') as fp:
        # fp.write(response.text)

    parser = Parser(io.StringIO(response.text))
    
    # All macros are defined at the top of the file,
    # so by the time parsing begins they are all defined
    # therefore we dont need to iterate over everything
    # as that needs to be done in a very specific way
    parser.parse()

    for k, v in parser._scanner.stream.preprocessor.defined.items():
        print(k, ''.join(v.resolve(parser._scanner.stream)))

get_styles()