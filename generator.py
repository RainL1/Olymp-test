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


def RandomString(n: int, alphabet: str = string.ascii_letters) -> str:
    _require_int("n", n)
    _require_non_negative("n", n)
    if not isinstance(alphabet, str):
        raise TypeError("alphabet must be str")
    if len(alphabet) == 0:
        raise ValueError("alphabet must be non-empty")
    return ''.join(choices(alphabet, k=n))


def RandomArray(n: int, minn: int, maxn: int, distinct: int = 0) -> list:
    _require_int("n", n)
    _require_int("minn", minn)
    _require_int("maxn", maxn)
    _require_int("distinct", distinct)
    _require_non_negative("n", n)
    _require_binary("distinct", distinct)
    if minn > maxn:
        raise ValueError("minn must be <= maxn")
    if distinct:
        if n > maxn - minn + 1:
            raise ValueError("n must be <= maxn - minn + 1 if distinct")
        return sample(range(minn, maxn + 1), n)
    return [randint(minn, maxn) for i in range(n)]


def RandomPermutation(n: int) -> list:
    _require_int("n", n)
    _require_non_negative("n", n)
    ret = [i for i in range(1, n + 1)]
    shuffle(ret)
    return ret


def ShuffleGraph(edges: list, n: int, idx: int = 0) -> None:
    if not isinstance(edges, list):
        raise TypeError("edges must be list")
    _require_int("n", n)
    _require_non_negative("n", n)
    _require_int("idx", idx)
    _require_binary("idx", idx)

    for edge in edges:
        if not isinstance(edge, list):
            raise TypeError("each edge must be list")
        if len(edge) != 2:
            raise ValueError("each edge must have exactly 2 vertices")
        for vertex in edge:
            _require_int("edge vertex", vertex)
            if vertex < idx or vertex > n - 1 + idx:
                raise ValueError(f"edge vertices must be in [{idx}, {n - 1 + idx}]")

    if n == 0 or len(edges) == 0:
        return

    shuffle(edges)
    perm = RandomPermutation(n)
    for e in edges:
        e[0], e[1] = perm[e[0] - idx] - 1 + idx, perm[e[1] - idx] - 1 + idx
        if RandomInt(0, 1):
            e[0], e[1] = e[1], e[0]


def RandomTree(n: int, idx: int = 0, mode: int = 1) -> list:
    _require_int("n", n)
    _require_int("idx", idx)
    _require_int("mode", mode)
    _require_non_negative("n", n)
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
    ShuffleGraph(edges, n, 0)
    if idx:
        for e in edges:
            e[0] += 1
            e[1] += 1
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

    # if m == 0 then m is random number
    user_unspecified_m = m == 0
    mode = randint(0, 10)
    if user_unspecified_m:
        if connected:
            m = randint(n - 1, max_edges)
        else:
            m = randint(0, max_edges)
    if connected and user_unspecified_m and mode == 0:
        return RandomTree(n, idx, mode=1)

    edges = []
    if m > max_edges // 2:
        pool = [[u, v] for u in range(n) for v in range(u + 1, n)]
        if connected:
            tree = RandomTree(n, 0, mode=1)
            tree_keys = {tuple(sorted(e)) for e in tree}
            pool = [e for e in pool if tuple(e) not in tree_keys]
            edges = tree + sample(pool, m - (n - 1))
        else:
            edges = sample(pool, m)
    else:
        seen = set()
        if connected:
            edges = RandomTree(n, 0, mode=1)
            for e in edges:
                seen.add(tuple(sorted(e)))
        while len(edges) < m:
            u = randint(0, n - 1)
            v = randint(0, n - 1)
            if u == v:
                continue
            key = (u, v) if u < v else (v, u)
            if key in seen:
                continue
            seen.add(key)
            edges.append([u, v])

    ShuffleGraph(edges, n, 0)
    if idx:
        for e in edges:
            e[0] += 1
            e[1] += 1
    return edges


def RandomDAG(n: int, idx: int = 0, m: int = 0) -> list:
    _require_int("n", n)
    _require_int("idx", idx)
    _require_int("m", m)
    _require_non_negative("n", n)
    _require_binary("idx", idx)
    _require_non_negative("m", m)

    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"m must be <= {max_edges}")
    if m == 0:
        m = randint(0, max_edges)
    if m > max_edges // 2:
        pool = [[u, v] for u in range(n) for v in range(u + 1, n)]
        edges = sample(pool, m)
    else:
        seen = set()
        edges = []
        while len(edges) < m:
            u = randint(0, n - 1)
            v = randint(0, n - 1)
            if u == v:
                continue
            key = (u, v) if u < v else (v, u)
            if key in seen:
                continue
            seen.add(key)
            edges.append([key[0], key[1]])

    perm = RandomPermutation(n)
    for e in edges:
        e[0], e[1] = perm[e[0]] - 1, perm[e[1]] - 1
    shuffle(edges)
    if idx:
        for e in edges:
            e[0] += 1
            e[1] += 1
    return edges


def AddWeights(edges: list, minw: int, maxw: int) -> None:
    if not isinstance(edges, list):
        raise TypeError("edges must be list")
    _require_int("minw", minw)
    _require_int("maxw", maxw)
    if minw > maxw:
        raise ValueError("minw must be <= maxw")
    for e in edges:
        if not isinstance(e, list):
            raise TypeError("each edge must be list")
        if len(e) != 2:
            raise ValueError("each edge must have exactly 2 vertices (before weighting)")
        e.append(randint(minw, maxw))


__all__ = [
    "RandomInt",
    "RandomString",
    "RandomArray",
    "RandomPermutation",
    "ShuffleGraph",
    "RandomTree",
    "RandomGraph",
    "RandomDAG",
    "AddWeights",
]
