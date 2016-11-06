from itertools import combinations
import pymc3 as pm
import numpy as np
from BayesAB.bayes_AB_conversion import BayesABConversion

class BayesAB():
    """
    Main class for BayesAB
    Currently just supports conversion class
    """
    
    



if __name__ == '__main__':
    ###Running with n and c defined
    bab = BayesABConversion()
    bab.fit(n=[1000,1000,1000],c=[500,450,400])
    print bab.trace