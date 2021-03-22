
from armaconfig import loads
from armaconfig.entry import EOL
from armaconfig.analyse import Parser

def get_styles():
    with open('tools/definitions.hpp') as fp:
        parser = Parser(fp)
        
        # All macros are defined at the top of the file,
        # so by the time parsing begins they are all defined
        # therefore we dont need to iterate over everything
        # as that needs to be done in a very specific way
        parser.parse()

        for k, v in parser._scanner.stream.preprocessor.defined.items():
            print(k, ''.join(v.resolve(parser._scanner.stream)))

get_styles()