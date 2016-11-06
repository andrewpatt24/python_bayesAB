from itertools import combinations
import pymc3 as pm
import numpy as np

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
    
    def __init__(self, model_type='heirarchical',sample=50000,burn=0):

        self.model_type = model_type

        self.sample = 50000
        self.burn = 0
    
    def _create_obs(self):

        self.obs = []
        self.idx = []
        
        for i in xrange(len(self.n)):
            #print n[i], c[i]
            self.obs += [1 for x in xrange(self.c[i])] + [0 for x in xrange(self.n[i] - self.c[i])]
            self.idx += [i for x in xrange(self.n[i])]
    
    def _heirarchical_model(self):
        
        with pm.Model() as model:
    
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

            step = pm.Metropolis()
            self.trace = pm.sample(self.sample, step=step)[self.burn:]

    def _simple_model(self):
        
        with pm.Model() as model:
    
            # Define distributions for each unknown 'true' probability 
            # - This is now being drawn from a uniform distribution
            p = pm.Uniform("p", 0,1,shape=len(self.n))
    
            # Define the deterministic function for each value
            for i, j in combinations(xrange(len(self.n)), 2):
                delta = pm.Deterministic("delta_"+str(i)+str(j), p[j]-p[i])

            # Set of observations, in this case we have two observation datasets.
            obs = pm.Bernoulli("obs", p[self.idx], observed=self.obs)

            step = pm.Metropolis()
            self.trace = pm.sample(self.sample, step=step)[self.burn:]

    def _run_model(self):

        if self.model_type=='heirarchical':
            self._heirarchical_model()

    def fit(self,n=None,c=None,idx=None,obs=None):
        """
        Create data if n/c is defined else assign idx and obs
        """
        self._check_fit_data(n,c,idx,obs)

        self.n = n
        self.c = c

        if self.n is None:
            self.idx=idx
            self.obs=obs
            self.n = len(self.idx)
            self.c = np.sum(self.obs)
        else:
            self._create_obs()

        self._run_model()
        ##end fit

    def traceplot(self):
        return pm.traceplot(self.trace)

    def _check_fit_data(self,n,c,idx,obs):
        """
        Check fit data and ive errors if incorrect
        """
        pass



if __name__ == '__main__':
    ###Running with n and c defined
    bab = BayesABConversion()
    bab.fit(n=[1000,1000,1000],c=[500,450,400])
    print bab.trace