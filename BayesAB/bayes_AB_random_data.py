import numpy as np


class BernoulliIterator():
	"""
	Used to create conversion data iteratively so simulations can be run
	Inititalised with p = True Probabiity of success/conversion
	iteratively add data with add_data(n) where n is the value you want to add
	"""

	def __init__(self,p,n=False):
		self.p = list(p)
		self.idx = []
		self.obs = []

		if n:
			self.add_data(n)

	def add_data(n=1000):
		for i, pp in enumerate(self.p):
			self.idx += [i for x in xrange(n)]
			self.obs += np.random.binomial(n, p=pp, size=n)




if __name__ == '__main__':
	random_data()