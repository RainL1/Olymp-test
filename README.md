Simple stress-testing for c++.

For version 1 works only with .cpp, but this may be improved in future
For using you just need to change `user.py` for your task, using included in `generator.py`
Example:
```
from generator import *

t = RandomInt(1, 50)
test = f"{t}\n"
for i in range(t):
    n = RandomInt(1, 50)
    test += f"{n}\n"
    a = RandomArray(n, -100, 100)
    for i in a:
        test += f"{i} "
    test += '\n'
    
print(test)
```
Generates random number of test sets with n and n-valued array;
After that you may run `main.py` using `python main.py --gen --good --bad --tests`, for default it is
user.py, good.cpp, bad.cpp, 1000

Features in `generator.py` for now:
"RandomInt",
"RandomArray",
"RandomPermutation",
"shuffleGraph",
"RandomTree",
"RandomGraph".

