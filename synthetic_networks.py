"""
Author: Gonzalo Contreras Aso
Last modification: 21/09/2022
Summary: Computation of the maximum alpha for PageRank full control, 
         maximum alpha for PageRank ranking control, and
         maximum beta for biplex PageRank ranking control
         for synthetic networks (random and scale-free).
"""

# Import standard network and data-science libraries
import numpy as np
import networkx as nx
import igraph as ig
import pandas as pd
from itertools import product
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import inv as sparse_inv
from scipy.sparse import identity as sparse_identity

# Import our own, custom functions
from utilities import *


## General function to gather all information of a network

def everything_together(G, sample=100, tol=1e-03, incr=0.001, power=3):
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

# Parameters of the synthetic networks generated
nodes = range(10, 20000, 1000)
probs = [0.3, 0.5]
sample = 10

## Random directed networks ##
print("## Random directed networks ##")
for n, p, s in product(nodes, probs, range(sample)):
    if s == 0:
        print(n, p)
    G = ig.Graph.Erdos_Renyi(n, p*10/n, directed=True)
    props, alphas = everything_together(G)

    network_stats[f'Random_{n}_{p*10/n}_{s}'] = list(props) + list(alphas)

print()

## Directed scale-free networks ##
# In this case we need to first generate them with networkx, 
# as igraph does not have an implementation for directed ones.
print("## Directed scale-free networks ##")
for n, p, s in product(nodes, probs, range(sample)):
    if s == 0:
        print(n, p)
    Gx = nx.scale_free_graph(n, alpha=p-0.05, beta=1-p, gamma=0.05)
    Gx = nx.DiGraph(Gx)
    G = ig.Graph.from_networkx(Gx)
    props, alphas = everything_together(G)

    network_stats[f'ScaleFree_{n}_{p}_{s}'] = list(props) + list(alphas)


## Save to csv with appropriate columns ##
df = pd.DataFrame.from_dict(network_stats, orient='index', columns = ['N', 'E', 'Directed?', 'Weighted?', 'alpha_f_PR', 'alpha_r_PR', 'beta_r_BPR'])
net_type = [name.split('_')[0] for name in df.index]
df['Type'] = net_type
df.round(6).to_csv('NetworkStats/synthetic_statistics.csv')
