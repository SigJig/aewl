
def inheritors(cls):
    subs = set()
    work = [cls]

    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subs:
                subs.add(child)
                work.append(child)

    return subs