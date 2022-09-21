"""
Author: Gonzalo Contreras Aso
Last modification: 21/09/2022
Summary: Computation of the maximum alpha for PageRank full control, 
         maximum alpha for PageRank ranking control, and
         maximum beta for biplex PageRank ranking control.
"""

# Import standard network and data-science libraries
import numpy as np
import networkx as nx
import igraph as ig
import pandas as pd
import os
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import inv as sparse_inv
from scipy.sparse import identity as sparse_identity

# Import our own, custom functions
from utilities import *


## General function to gather all information of a network

def everything_together(G, sample=100, tol=1e-03, incr=0.01, power=3):
    '''
    From a directed graph, undangle it, obtain its P-matrix, compute
    the maximum alpha for full/rank control in the standard
    PageRank, and the maximum beta for rank control in the biplex case.
    '''

    # Basic network properties
    props = basic_props(G)
    
    # Add a random outlink from dangling nodes
    P = undangled_P(G)

    # Compute alphas and beta
    alpha_full_PR, alpha_rank_PR = alphas_PR(P, sample, tol)
    beta_rank_BPR = beta_BPR(P, incr, power)

    alphas = (alpha_full_PR, alpha_rank_PR, beta_rank_BPR)

    return props, alphas


network_stats = {}

## Directed, weighted networks ##
print("## Directed, weighted ##")

pathDW = 'Datasets/DW/'
filesDW = os.listdir(pathDW)
filesDW.sort()

# Go file by file, loading their network and using above function 
for file in filesDW:
    name = file.split('.graphml')[0]
    print('Processing', name)
    G = ig.read(pathDW + file, format='graphml')
    props, alphas = everything_together(G)

    network_stats[name] = list(props) + list(alphas)

print()

## Directed, unweighted networks ##
print("## Directed, unweighted ##")

pathDU = 'Datasets/DU/'
filesDU = os.listdir(pathDU)
filesDU.sort()

# Go file by file, loading their network and using above function 
for file in filesDU:
    name = file.split('.graphml')[0]
    print('Processing', name)
    G = ig.read(pathDU + file, format='graphml')
    props, alphas = everything_together(G)

    network_stats[name] = list(props) + list(alphas)


## Save to csv with appropriate columns ##

df = pd.DataFrame.from_dict(network_stats, orient='index', columns = ['N', 'E', 'Directed?', 'Weighted?', 'alpha_f_PR', 'alpha_r_PR', 'alpha_r_BPR'])
df.round(6).to_csv('NetworkStats/real_statistics.csv')


