from os import path

rp = path.dirname(path.realpath(__file__))


def abpath(*args, fp=rp):
    return path.join(fp, *args)
