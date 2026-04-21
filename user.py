from generator import *

t = RandomInt(1, 50)
test = f"{t}\n"
for i in range(t):
    n = RandomInt(1, 50)
    test += f"{n}\n"
    a = RandomArray(n, -100, 100)
    for x in a:
        test += f"{x} "
    test += '\n'
    
print(test)