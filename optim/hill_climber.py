import random

class HillClimber:

    def __init__(self, space, eval):
        """Space is a list of (key, values). Eval is a function."""
        self._length = len(space)
        self._keys = tuple(space[i][0] for i in range(self._length))
        self._values = tuple(space[i][1] for i in range(self._length))
        self._eval = eval
        self._count = 0
        self._cache = dict()

    def _random(self):
        """Creates a random candidate."""
        def generator():
            for values in self._values:
                yield random.randint(0, len(values) - 1)
        return tuple(generator())

    def _neighbors(self, candidate):
        """Iterates over all the neighbors of a candidate."""
        def generator():
            for i in range(self._length):
                # Left neighbor
                neighbor = list(candidate)
                neighbor[i] -= 1
                if neighbor[i] >= 0:
                    yield tuple(neighbor)
                # Right neighbor
                neighbor = list(candidate)
                neighbor[i] += 1
                if neighbor[i] < len(self._values[i]):
                    yield tuple(neighbor)
        neighbors = list(generator())
        random.shuffle(neighbors)
        return tuple(neighbors)

    def _params(self, candidate):
        """Formats a candidate as a dict."""
        params = dict()
        for i in range(self._length):
            params[self._keys[i]] = self._values[i][candidate[i]]
        return params

    def _eval_cache(self, candidate):
        """Evaluates a candidate."""
        if candidate not in self._cache:
            self._count += 1
            params = self._params(candidate)
            score = self._eval(**params)
            self._cache[candidate] = score
        return self._cache[candidate]

    def climb(self, max_iter=100):
        """Runs a random hill-climbing iteration."""
        best_candidate = self._random()
        best_score = self._eval_cache(best_candidate)
        yield best_score, self._params(best_candidate)
        while True:
            for candidate in self._neighbors(best_candidate):
                if self._count >= max_iter:
                    return
                score = self._eval_cache(candidate)
                if score < best_score:
                    best_candidate = candidate
                    best_score = score
                    yield best_score, self._params(best_candidate)
                    break
            else:
                return

    def shotgun_climb(self, max_iter=100):
        """Runs hill-climbing iterations."""
        best_score = None
        while self._count < max_iter - 1:
            for score, params in self.climb(max_iter):
                if best_score is None or score < best_score:
                    best_score = score
                    yield best_score, params


# Test

def rosenbrock(x, y):
    return pow(1 - x, 2) + 100 * pow(y - pow(x, 2), 2)

hc = HillClimber(
    space=[
        ('x', [0.1 * x for x in range(-100, 101)]),
        ('y', [0.1 * x for x in range(-100, 101)]),
    ],
    eval=rosenbrock)

for score, params in hc.shotgun_climb(500):
    print(score, params)
