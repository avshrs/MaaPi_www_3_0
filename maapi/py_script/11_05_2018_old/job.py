

from decimal import Decimal

def z1(code1, code2):
    parse = lambda x: int(x.replace('-', ''))
    code1, code2 = parse(code1), parse(code2)
    return ["%02d-%03d" % divmod(x, 1000) for x in range(code1 + 1, code2)]

def z2(ns, n):
    return list(set(range(n)) - set(ns))

def z3():
    return [Decimal(20 + x * 5) / 10 for x in range(8)]

print(z1("79-900", "80-155"))
print(z2([1, 3, 4, 5, 6, 7, 8], 10))
print(z3())
