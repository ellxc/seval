x = 1
x += 2
c = 4
b = c+x
print("x ",x)
print("c ",c)
print("b ", b)
print(f"x {x}")

def f(x):
    return x + 12

print(f(56))

c = 1
def x(a):
    return a+c

print(x(2))

c = 1
def a():
    c = 2
    def b():
        c = 3
        return c
    return b()

print(a())

z = 1
while z < 6:
    z += 1
else:
    z += 4

print(z)


for x in [1,2,3]:
    z += x
    print(z)
else:
    pass

print(z)

def zxc():
    for x in [1,2,3]:
        if x is 2:
            return "two"

print(zxc())

print(lambda x, y: x + y)