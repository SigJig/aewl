
from pathlib import Path
from armaconfig import dumps, dump, load
from .parser import parse

def _export_w_base(src, name, parent=None):
    un = parse(src, name)
    un.process_all()

    if parent is None:
        parent = get_base()

    return un.export(parent=parent)

def get_base():
    with open(Path(__file__).parent.absolute().joinpath('defines.hpp')) as fp:
        return load(fp)

def file_to_file(src, *args, **kwargs):
    return str_to_file(src.read(), *args, **kwargs)

def str_to_file(src, dst, *args, **kwargs):
    name = kwargs.get('name', '')

    if 'parent' in kwargs:
        parent = kwargs.pop('parent')
    else:
        parent = None

    return dump(_export_w_base(src, name, parent=parent), dst, *args, **kwargs)

def file_to_str(src, *args, **kwargs):
    return str_to_str(src.read(), *args, **kwargs)

def str_to_str(src, *args, **kwargs):
    name = kwargs.get('name', '')

    if 'parent' in kwargs:
        parent = kwargs.pop('parent')
    else:
        parent = None

    return dumps(_export_w_base(src, name, parent=parent), *args, **kwargs)