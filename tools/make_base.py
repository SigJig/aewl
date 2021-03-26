
import re
import json
from collections import defaultdict
from armaconfig import loads, load, dump
from armaconfig.entry import EOL
from armaconfig.config import Config
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


def dump_configs():
    with open('tools/definitions.hpp') as fp:
        loaded = load(fp)
        basic = None

        for k in iter(loaded):
            if basic is None:
                if k == 'aewl_basics':
                    basic = loaded[k]
                    continue
                else:
                    raise Exception()

            conf = loaded[k]
            iterator = iter(conf._dict.copy())

            for ck in iterator:
                if ck in basic:
                    conf.pop(ck)

            if 'type' in conf:
                if conf.inherits is None:
                    conf.add_inherits('aewl_basics') # adds only to rscs

            conf.name = re.sub(r'^Rsc(\w+)$', lambda x: 'aewl_{}'.format(x.group(1)), conf.name)
            conf.name = conf.name.lower()

        with open('tools/configs.githide.hpp', 'w') as wp:
            """ dct = {}

            for k in iter(loaded):
                if 'type' not in loaded[k]:
                    continue # skip things like attributes

                n = re.sub(r'^rsc(\w+)$', lambda x: x.group(1).lower(), k)

                dct[n] = loaded[k].to_dict()
            """
            dump(loaded, wp, indent=4)

dump_configs()