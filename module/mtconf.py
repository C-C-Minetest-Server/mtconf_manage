import re

re_rule = re.compile(r"^(#?\w+) *= *(.+)$",flags=(re.M))

def fromfile(f):
    return read(f.read())

def read(t):
    m = re_rule.findall(t)
    RDCT = {}
    for x in m:
        RDCT[x[0]] = x[1]
    return RDCT

def render(d):
    RSTR = ""
    for x in d:
        RSTR = RSTR + x + " = " + d[x] + "\n"
    return RSTR

def write(f,d):
    f:write(render(d))
