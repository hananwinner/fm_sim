from typing import Tuple, Optional
import numpy
import time

# This values should not be changed.
X_MIN = -2000
X_MAX = 6000
X_RES = 20

def generate_thresholds(x: numpy.ndarray,
                         labels: numpy.ndarray,
                         resolution: int = X_RES,
                         x_min: int = X_MIN,
                         x_max: int = X_MAX) -> numpy.ndarray:
    unique_labels = sorted(numpy.unique(labels))
    num_labels = len(unique_labels)
    threshold_options = numpy.arange(x_min + resolution / 2,
                                     x_max,
                                     resolution)
    scores = dict()

    def _gen_thr(l1: int, l2):
        assert l2 > l1
        if (l1, l2) in scores:
            return scores[(l1, l2)]
        if l2 - l1 == 1:
            best = numpy.inf
            threshold = None
            for t in threshold_options:
                erros_l1 = numpy.sum(numpy.logical_and(x > t, labels <= unique_labels[l1]))
                erros_l2 = numpy.sum(numpy.logical_and(x < t, labels >= unique_labels[l2]))
                errors = erros_l1 + erros_l2
                if errors < best:
                    best = errors
                    threshold = t
            scores[(l1, l2)] = best, [threshold]
            return best, [threshold]
        else:
            best = numpy.inf
            thresholds = []
            for l_mid in range(l1 + 1, l2):
                score_low, threshold_low = _gen_thr(l1, l_mid)
                score_high, thresholds_high = _gen_thr(l_mid, l2)
                score = score_low + score_high
                if score < best:
                    best = score
                    thresholds = threshold_low + thresholds_high
            scores[(l1, l2)] = best, thresholds
            return best, thresholds

    score, thresholds = _gen_thr(0, num_labels - 1)
    return thresholds


def generate_data(num_labels: int,
                  resolution: int = X_RES,
                  x_min: int = X_MIN,
                  x_max: int = X_MAX) -> Tuple[numpy.ndarray, numpy.ndarray]:
    assert 16 >= num_labels >= 4
    size = 2 ** 17
    labels = numpy.random.randint(0, num_labels, size)
    delta = (x_max - x_min) / num_labels
    x = x_min + labels * delta
    x += 0.1 * delta * numpy.random.randn(size)
    x = (0.8 - 0.05 * numpy.random.rand(size)) * x
    x = numpy.clip(resolution * (x / resolution).astype(int), x_min, x_max)
    return x, labels


if __name__ == "__main__":
    x, labels = generate_data(16)
    tic = time.time()
    thresholds = generate_thresholds(x, labels)
    toc = time.time()
    print(f"took = {toc - tic:.3f} seconds")
