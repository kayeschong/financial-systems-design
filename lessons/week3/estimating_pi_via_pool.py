# An illustration of multiprocessing.Pool, a higher-level alternative to
# threading.  Our specific example is estimating pi via Monte Carlo
# integration, using concurrency to increase the accuracy of our estimate.

# Importantly, using multiprocessing.Pool gives us parallelism as well as
# concurrency, *even in CPython*:
# "The multiprocessing package offers both local and remote concurrency,
# effectively side-stepping the Global Interpreter Lock by using subprocesses
# instead of threads. Due to this, the multiprocessing module allows the
# programmer to fully leverage multiple processors on a given machine."

# This problem is well suited for a concurrent approach, because the workers
# do not need to communicate with each other, and very little data needs
# to be transmitted to, and returned from, each worker.

from multiprocessing import cpu_count, Pool, Value, Array


# A Windows-specific hack to ensure "estimates" and "N" are visible to the
# workers as intended.  c.f.
# https://stackoverflow.com/questions/39322677/python-how-to-use-value-and-array-in-multiprocessing-pool
def init(aa, vv):
    global estimates, N
    estimates = aa
    N = vv


# We would like to avoid the above hack entirely by simply passing "estimates"
# and "N" to pi_estimator() as arguments.  But, as the StackOverflow article
# explains:
#   "multiprocessing (mp) uses different pickler/unpickler mechanisms for
#   functions passed to most Pool methods. It's a consequence that objects
#   created by things like mp.Value, mp.Array, mp.Lock, ..., can't be passed
#   as arguments to such methods, although they can be passed as arguments
#   to mp.Process and to the optional initializer function of mp.Pool()."
def pi_estimator(idx):
    from random import random
    xs = [random() for i in range(N.value)]
    ys = [random() for i in range(N.value)]
    # Double-check that the xs and ys are uncorrelated:
    # mean_xs = sum(xs) / N.value
    # mean_ys = sum(ys) / N.value
    # cov = sum((x - mean_xs) * (y - mean_ys) for
    #           (x, y) in zip(xs, ys)) / N.value
    # print('Sample covariance of xs and ys:', cov)  # Should be close to 0.
    num_hits = sum([1 for (x, y) in zip(xs, ys) if x*x + y*y <= 1.0])
    estimates[idx] = 4.0 * num_hits / N.value


if __name__ == "__main__":
    num_cores = cpu_count()
    print('Number of cores:', num_cores)

    estimates = Array('d', [0.0] * num_cores)
    N = Value('i', 10000000)

    # Notwithstanding the hacks and limitations mentioned above, we get the
    # concurrency we are after with just two lines of code:
    with Pool(num_cores, initializer=init, initargs=(estimates, N)) as pool:
        pool.map(pi_estimator, range(num_cores))

    print('Sub-estimates:', ', '.join([str(est) for est in estimates]))
    estimate = sum(estimates) / num_cores
    print('Estimated value of pi:', estimate)
