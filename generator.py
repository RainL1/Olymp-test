from random import *


def RandomInt(minn: int, maxn: int) -> int:
    return randint(minn, maxn)


def RandomArray(n: int, minn: int, maxn: int) -> list:
    return [randint(minn, maxn) for i in range(n)]


def RandomPermutation(n: int) -> list:
    ret = [i for i in range(1, n + 1)]
    shuffle(ret)
    return ret


def shuffleGraph(edges: list) -> None:
    if len(edges) == 0:
        return

    idx = 0
    for edge in edges:
        if 0 in edge:
            idx = 0
            break
    else:
        idx = 1

    n = max(max(edge) for edge in edges) - idx + 1
    shuffle(edges)
    perm = RandomPermutation(n)
    for i in edges:
        i[0], i[1] = perm[i[0] - idx] - 1 + idx, perm[i[1] - idx] - 1 + idx
        if RandomInt(0, 1):
            i[0], i[1] = i[1], i[0]


def RandomTree(n: int, idx: int = 0, mode: int = 1) -> list:
    # tree in form of [[u_i, v_i]]
    edges = []
    if mode == 1:
        for i in range(n - 1):
            edges.append([randint(0, i), i + 1])
    else:
        base = max(1, n // 3)
        for i in range(1, base):
            edges.append([i, i - 1])
        for i in range(base, n):
            edges.append([randint(0, i - 1), i])
    shuffleGraph(edges)
    if idx:
        for i in range(n - 1):
            edges[i][0] += 1
            edges[i][1] += 1
    return edges


def RandomGraph(n: int, idx: int = 0, connected: int = 1, m: int = 0) -> list:
    # Not good for now for big graphs i think, just for stress for WA
    # if m == 0 then m is random number
    # should be diff in future 
    mode = randint(0, 10)
    edges = []
    if m == 0:
        if connected:
            m = randint(n - 1, n * (n - 1) // 2)
        else:
            m = randint(0, n * (n - 1) // 2)
    if connected and mode == 0:
        return RandomTree(n, idx, mode=1)
    if connected:
        edges = RandomTree(n, 0, mode=1)
    while len(edges) < m:
        u = randint(0, n - 1)
        v = randint(0, n - 1)
        if u != v and [u, v] not in edges and [v, u] not in edges:
            edges.append([u, v])
    shuffleGraph(edges)
    if idx:
        for i in range(len(edges)):
            edges[i][0] += 1
            edges[i][1] += 1
    return edges


__all__ = [
    "RandomInt",
    "RandomArray",
    "RandomPermutation",
    "shuffleGraph",
    "RandomTree",
    "RandomGraph",
]
