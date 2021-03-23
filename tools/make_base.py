
import json
from collections import defaultdict
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
        next(parser.parse())
        out = defaultdict(dict)

        stream = parser._scanner.stream

        for k, v in stream.preprocessor.defined.items():
            split = k.split('_')
            section = split[0].lower()

            out[section]['_'.join(split[1:])] = ''.join(v.resolve(stream)).strip()

        with open('out.githide', 'w') as wp:
            for section, vs in out.items():
                wp.write('\n# {}\n'.format(section))

                for k, v in vs.items():
                    wp.write('{} = {}\n'.format(k, str(v)))



get_styles()