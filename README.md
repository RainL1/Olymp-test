Simple stress-testing for c++.

For version 1 works only with .cpp, but this may be improved in future.
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
    for x in a:
        test += f"{x} "
    test += '\n'
    
print(test)
```
Generates random number of test sets with n and n-valued array;
After that you may run `main.py` using `python main.py --gen --good --bad --tests`, for default it is
user.py, good.cpp, bad.cpp, 1000

Features in `generator.py` for now:
- `RandomInt(minn, maxn)` — random int in `[minn, maxn]`.
- `RandomString(n, alphabet=string.ascii_letters)` — random string of length `n` from given alphabet.
- `RandomArray(n, minn, maxn, distinct=0)` — array of `n` ints in `[minn, maxn]`; `distinct=1` gives array with all diff vals (requires `n <= maxn - minn + 1`).
- `RandomPermutation(n)` — random permutation of `1..n`.
- `ShuffleGraph(edges, n, idx=0)` — shuffles edges, changes perm of `n` verteces, swap u, v randomly
- `RandomTree(n, idx=0, mode=1)` — random tree on `n` vertices as list of edges `[[u, v], ...]`. mode=1 is for random parent picker method, mode=2 is big depth(>=n/3)
- `RandomGraph(n, idx=0, connected=1, m=0)` — random simple graph with `m` edges (`m=0` picks `m` randomly).
- `RandomDAG(n, idx=0, m=0)` — random DAG with `m` edges (`m=0` picks `m` randomly). 
- `AddWeights(edges, minw, maxw)` — appends a random weight in `[minw, maxw]` to each edge `[u, v]` → `[u, v, w]`. Works for tree, graph, DAG.

`idx` parameter is binary: `0` for 0-indexed output, `1` for 1-indexed.

