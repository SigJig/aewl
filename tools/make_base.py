
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


def remove_redundant():
    def _to_dict(conf):
        return {k: basic[k] for k in basic}

    def _remove(conf, check, out=defaultdict(dict)):
        for name, v in conf:
            if name not in check:
                if isinstance(v, Config):
                    v = _to_dict(v) # _remove(_to_dict(v).items(), check)

                out[k][name] = v

        return out


    with open('tools/definitions.hpp') as fp:
        loaded = load(fp)
        basic = None

        for k in loaded:
            if basic is None:
                if k == '_basics':
                    basic = loaded[k]
                    continue
                else:
                    raise Exception()

            conf = loaded[k]
            iterator = iter(conf._dict.copy())

            for ck in iterator:
                if ck in basic:
                    conf.pop(ck)

        with open('tools/definitions_new.hpp', 'w') as wp:
            dump(loaded, wp, indent=4)


remove_redundant()