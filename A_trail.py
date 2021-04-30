# -*- coding: utf-8 -*-

a = 2.3
r1 = isinstance(a, int)
r2 = isinstance(a, float)
r3 = isinstance(a, (str, float, list))
print(r1, r2, r3)

