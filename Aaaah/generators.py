from .primitives import *

class _SubscriptableGenerator():
	def __init__(self, generator, *args):
		self.gen = generator(*args)

	def __getitem__(self, key):
		try:
			if isinstance(key, int):
				self.ignore(key)
				yield next(self.gen)
			else:
				step = key.step if key.step else 1
				start = key.start if key.start else 0

				i = start
				self.ignore(start)

				while i < key.stop:
					yield next(self.gen)
					i = i + step
					self.ignore(step-1)
		except Exception:
			self.raiseInvalidSlice(key)

	def raiseInvalidSlice(self, key):
		raise KeyError("{0} n'est pas une slice valide.".format(key))

	def ignore(self, n):
		for i in range(n):
			next(self.gen)

def _Row(shape, X, Y, interval):
	i = 0
	while True:
		yield lambda thickness, *args: shape(thickness, X + i, Y, *args)
		i += interval


def Row(*args):
	return _SubscriptableGenerator(_Row, *args)
