a = None
b = 4.0
c = 5.0

if a is None:
    a = (c**2 - b**2)**0.5

if b is None:
    b = (c**2 - a**2)**0.5

if c is None:
    c = (a**2 + b**2)**0.5

print(f"a = {a}, b = {b}, c = {c}")