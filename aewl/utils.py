
def inheritors(cls, include_cls=False):
    if include_cls:
        subs = set([cls])
    else:
        subs = set()

    work = [cls]

    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subs:
                subs.add(child)
                work.append(child)

    return subs

def dictmerge(dest, src):
    for key, value in src.items():
        if isinstance(value, dict):
            dest_val = dest.setdefault(key, {})
            
            dictmerge(dest_val, value)
        else:
            dest[key] = value

    return dest
