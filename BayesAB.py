from itertools import combinations


class BayesABConversion():
    """
    Class for Bayesian conversion tests
    Currently works with Heirarchical model and weak priors, using Metropolis to sample values
    
    Initial Values:
    sample: How many MCMC samples to take
    burn: How many initial sample to burn

    fit Values:
    n - list of cohort sizes of variants
    c - list of number of users converting/retatining/whatever
    
    outputs: 
    obj.trace gives traces to be used with other pymc3 plots etc.
    """
    
    def __init__(self, sample=50000,burn=0):
        
        self.obs = []
        self.idx = []

        self.sample = 50000
        self.burn = 0
    
    def _create_obs(self):
        
        for i in xrange(len(self.n)):
            #print n[i], c[i]
            self.obs += [1 for x in xrange(self.c[i])] + [0 for x in xrange(self.n[i] - self.c[i])]
            self.idx += [v for x in xrange(self.n[i])]
    
    def _heirarchical_model(self):
        
        with pm.Model() as self.model:
    
            ##hyper parameters
            hyper_mu = pm.Uniform('hyper_mu',0,1)
            hyper_sd = pm.Uniform('hyper_sd',0,np.sqrt(hyper_mu*(1-hyper_mu)))
    
            # Define distributions for each unknown 'true' probability 
            # - This is now being drawn from the distributions with the same hyper parameter distribution
            p = pm.Beta("p", mu=hyper_mu, sd=hyper_sd, shape=len(self.n))
    
            # Define the deterministic function for each value
            for i, j in combinations(xrange(len(self.n)), 2):
                delta = pm.Deterministic("delta_"+str(i)+str(j), p[j]-p[i])

            # Set of observations, in this case we have two observation datasets.
            obs = pm.Bernoulli("obs", p[self.idx], observed=self.obs)

    def _run_model(self,model):

            _create_obs()
            _heirarchical_model()

            step = pm.Metropolis()
            self.trace = model.sample(50000, step=step)

    def fit(self,n,c):

        self.n = n
        self.c = c

        _run_model()



if __name__ == '__main__':
    bab = BayesABConversion()
    bab.fit([1000,1000,1000],[500,450,400])
    print bab.trace