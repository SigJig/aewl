
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