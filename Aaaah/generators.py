from .primitives import *

class _SubscriptableGenerator():
	def __init__(self, generator, *args):
		self.gen = generator
		self.args = args

	def __getitem__(self, key):
		if isinstance(key, slice):
			if not key.stop:
				self.raiseInvalidSlice()
			stop = key.stop
			start = key.start if key.start else 0
			step = key.step  if key.step else 1

			if start < 0 or stop - start < 0 or step < 1:
				self.raiseInvalidSlice()

			i = 0
			for val in self.gen(*self.args):
				if i >= start:
					yield val
					start = i + step
				i = i + 1
				if i == stop:
					break
		else:
			try:
				i = 0
				for val in self.gen(*self.args):
					if i != key:
						pass
					else:
						yield val
						break
			except Exception:
				self.raiseInvalidSlice()

	def raiseInvalidSlice(self, key):
		raise KeyError("[{0}:{1}] n'est pas une slice valide.".format(key.start, key.stop))


def _Row(shape, X, Y, interval):
	i = 0
	while True:
		yield lambda thickness, *args: shape(thickness, X + i, Y, *args)
		i += interval


def Row(*args):
	return _SubscriptableGenerator(_Row, *args)
