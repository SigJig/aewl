
from pathlib import Path
from armaconfig import dumps, dump, load
from .parser import parse
from .context import Context

def _export(src, name, path_parent=None, parent=None):
    un = parse(src, name, path_parent)
    ctx = Context(un, parent_export=parent)
    ctx.process_all()

    # return un.export(parent=parent)
    return ctx.export

def _resolve_kwargs(kwargs):
    def _pop_or_none(k):
        if k in kwargs:
            return kwargs.pop(k)

        return None

    return {
        'path_parent': _pop_or_none('path_parent'),
        'parent': _pop_or_none('parent')
    }, kwargs    

def file_to_file(src, *args, **kwargs):
    kwargs['path_parent'] = Path(src.name).parent.absolute()

    return str_to_file(src.read(), *args, **kwargs)

def str_to_file(src, dst, *args, **kwargs):
    name = kwargs.get('name', '')
    popped_args, kwargs = _resolve_kwargs(kwargs)

    return dump(_export(src, name, **popped_args), dst, *args, **kwargs)

def file_to_str(src, *args, **kwargs):
    kwargs['path_parent'] = Path(src.name).parent.absolute()

    return str_to_str(src.read(), *args, **kwargs)

def str_to_str(src, *args, **kwargs):
    name = kwargs.get('name', '')
    popped_args, kwargs = _resolve_kwargs(kwargs)

    return dumps(_export(src, name, **popped_args), *args, **kwargs)
