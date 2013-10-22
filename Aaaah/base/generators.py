from itertools import islice

class _Sliceable(object):
    """Sliceable(iterable) is an object that wraps 'iterable' and
    generates items from 'iterable' when subscripted. For example:

        >>> from itertools import count, cycle
        >>> s = Sliceable(count())
        >>> list(s[3:10:2])
        [3, 5, 7, 9]
        >>> list(s[3:6])
        [13, 14, 15]
        >>> next(Sliceable(cycle(range(7)))[11])
        4
        >>> s['string']
        Traceback (most recent call last):
            ...
        KeyError: 'Key must be non-negative integer or slice, not string'

    """
    def __init__(self, iterable):
        self.iterable = iterable

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return islice(self.iterable, key, key + 1)
        elif isinstance(key, slice):
            return islice(self.iterable, key.start, key.stop, key.step)
        else:
            raise KeyError("Key must be non-negative integer or slice, not {}"
                           .format(key))

def _row(shape, X, Y, interval):
	i = 0
	while True:
		yield lambda thickness, *args: shape(thickness, X + i, Y, *args)
		i += interval


def row(*args):
	return _Sliceable(_row(*args))
