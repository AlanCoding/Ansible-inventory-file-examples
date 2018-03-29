import textwrap
from contextlib import contextmanager
import time


@contextmanager
def timeit(s=''):
    start = time.time()
    yield 1
    print s + ' {0:.6f} sec'.format(time.time() - start)


with timeit('create long variable '):
    var = 'x'*10**4


with timeit('wrap it 180 '):
    textwrap.wrap(var, 180)

