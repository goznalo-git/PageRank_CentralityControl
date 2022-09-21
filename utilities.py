'''
Author: Gonzalo Contreras Aso
Date: 21/09/2022
Summary: Collection of functions used in the main
         python programs.
'''

import numpy as np
import igraph as ig
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.linalg import inv as sparse_inv
from scipy.sparse import identity as sparse_identity
        

## General Functions ##

def undangled_P(G):
    '''
    Given a DiGraph G, add random out_links on danling nodes, 
    then return the row-normalize adjacency matrix.
    '''
    
    assert G.is_directed()
    
    N = len(G.vs())
    
    # Check the out-degree of each vertex and if zero, add a random link.
    for vertex in G.vs():
        if len(vertex.out_edges()) == 0:
            if G.is_weighted():
                G.add_edge(vertex.index, np.random.randint(0,N), weight=1.0)
            else:
                G.add_edge(vertex.index, np.random.randint(0,N))
                
    # Get the sparse adjacency matrix
    if G.is_weighted():
        A = G.get_adjacency_sparse(attribute='weight')
    else:
        A = G.get_adjacency_sparse()
    
    # Normalize by rows
    P = normalize(A, norm='l1').tocsc()
    
    return P


def basic_props(G):
    '''
    Given a graph G, return its basic properties:
    number of nodes, edges, directedness and weightedness.
    '''
    
    N = len(G.vs())
    E = len(G.es())
    directed = G.is_directed()
    weighted = G.is_weighted()

    return (N, E, directed, weighted)


## Standard PageRank ##

def alphas_PR(P, sample=100, tol=1e-03):
    '''
    Given a row-normalized adjacency matrix P, obtain the maximum alphas
    available for full control and ranking control
    For full control, we use a 'sample' of random centrality vectors in
    order to obtain an approximation.
    '''
    
    # Generate random centrality vectors and their corresponding alphas
    alpha_full_PR = P.shape[0] # Initialize a high alpha
    for _ in range(sample):
        pi0 = np.random.random(P.shape[0])
        
        # For each centrality vector, solve the n (in)equations for maximum alphas        
        for j in range(P.shape[0]):
            # Dot product with e_j is the same as selecting the jth element.
            RHS = P.transpose().dot(pi0)[j]
            LHS = pi0[j]
            
            if RHS < 0 or LHS < 0:
                print(LHS, RHS)
                raise Exception("Something went wrong.")
            
            if RHS == 0:
                continue
                
            if LHS/RHS < alpha_full_PR:
                alpha_full_PR = LHS/RHS                
                
            if alpha_full_PR < tol:
                break
                
    ## Now, ranking control alpha
    sumP = P.sum(axis=0)
    alpha_rank_PR = 1/np.max(sumP)
    
    return alpha_full_PR, alpha_rank_PR


## Biplex PageRank ##

def compute_calP(P, beta, power=3):
    '''
    Compute the calligraphic P matrix of the Biplex PageRank case
    If power is an integer, it is computed up to that power of the 
    resolvent series rather than by inverting the sparse matrix 
    (veeery useful for huge graphs).
    '''
    
    if power:
        power_inverse = sparse_identity(P.shape[0])
        # Truncated series sum method
        for n in range(1, power + 1):
            power_inverse += (beta/(1+beta) * P) ** n
        calP = (2-beta)/(1+beta) * power_inverse
    else:
        # Sparse inverse method
        to_invert = sparse_identity(P.shape[0]) + beta/(1+beta) * P
        calP = (2-beta)/(1+beta) * sparse_inv(to_invert)

    return calP

def beta_BPR(P, incr=0.01, power=3):
    '''
    Compute by brute force the beta required for ranking control of
    the biplex PR, increasing beta by 'incr' until the sign changes.
    '''
    
    beta_rank_BPR = 0
    calP = compute_calP(P, beta_rank_BPR, power)
    sumP = calP.sum(axis=0)
    
    # Evaluate until the sign changes.
    while 1 - beta_rank_BPR * np.max(sumP) > 0:
        beta_rank_BPR += incr
        calP = compute_calP(P, beta_rank_BPR, power)
        sumP = calP.sum(axis=0)
    
    return beta_rank_BPR - incr/2 # Small adjustment -> (beta above + beta below)/2
