from random import *
import string

def _require_int(name: str, value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be int")


def _require_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _require_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be > 0")


def _require_binary(name: str, value: int) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1")


def RandomInt(minn: int, maxn: int) -> int:
    _require_int("minn", minn)
    _require_int("maxn", maxn)
    if minn > maxn:
        raise ValueError("minn must be <= maxn")
    return randint(minn, maxn)

def RandomString(n: int) -> str:
    return ''.join(random.choices(string.ascii_letters, n))


def RandomArray(n: int, minn: int, maxn: int) -> list:
    _require_int("n", n)
    _require_int("minn", minn)
    _require_int("maxn", maxn)
    _require_non_negative("n", n)
    if minn > maxn:
        raise ValueError("minn must be <= maxn")
    return [randint(minn, maxn) for i in range(n)]


def RandomPermutation(n: int) -> list:
    _require_int("n", n)
    _require_non_negative("n", n)
    ret = [i for i in range(1, n + 1)]
    shuffle(ret)
    return ret


def shuffleGraph(edges: list, idx: int = 0) -> None:
    if not isinstance(edges, list):
        raise TypeError("edges must be list")
    _require_int("idx", idx)
    _require_binary("idx", idx)

    for edge in edges:
        if not isinstance(edge, list):
            raise TypeError("each edge must be list")
        if len(edge) != 2:
            raise ValueError("each edge must have exactly 2 vertices")
        for vertex in edge:
            _require_int("edge vertex", vertex)
            if vertex < 0:
                raise ValueError("edge vertices must be >= 0")

    if len(edges) == 0:
        return

    n = max(max(edge) for edge in edges) - idx + 1
    shuffle(edges)
    perm = RandomPermutation(n)
    for i in edges:
        i[0], i[1] = perm[i[0] - idx] - 1 + idx, perm[i[1] - idx] - 1 + idx
        if RandomInt(0, 1):
            i[0], i[1] = i[1], i[0]


def RandomTree(n: int, idx: int = 0, mode: int = 1) -> list:
    _require_int("n", n)
    _require_int("idx", idx)
    _require_int("mode", mode)
    _require_positive("n", n)
    _require_binary("idx", idx)
    if mode not in (1, 2):
        raise ValueError("mode must be 1 or 2")

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
    shuffleGraph(edges, idx)
    if idx:
        for i in range(n - 1):
            edges[i][0] += 1
            edges[i][1] += 1
    return edges


def RandomGraph(n: int, idx: int = 0, connected: int = 1, m: int = 0) -> list:
    _require_int("n", n)
    _require_int("idx", idx)
    _require_int("connected", connected)
    _require_int("m", m)
    _require_non_negative("n", n)
    _require_binary("idx", idx)
    _require_binary("connected", connected)
    _require_non_negative("m", m)

    if connected and n == 0:
        raise ValueError("connected graph must have at least 1 vertex")

    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"m must be <= {max_edges}")
    if connected and m != 0 and m < n - 1:
        raise ValueError("connected graph must have at least n - 1 edges")

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
    shuffleGraph(edges, idx)
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
    "RandomString",
]
