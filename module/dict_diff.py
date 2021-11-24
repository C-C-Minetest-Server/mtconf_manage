import os
def diff(o,n):
    os, ns = set(o.items()), set(n.items())
    return dict(os - ns), dict(ns - os)

def diff_str(o,n):
    print(o,n)
    dels,adds = diff(o,n)
    print("-" * 10)
    for x in dels:
        print("+ " + x + " = " + dels[x])
    print("-" * 10)
    for x in adds:
        print("+ " + x + " = " + adds[x])
    print("-" * 10)
