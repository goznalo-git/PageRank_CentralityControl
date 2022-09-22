"""
Author: Gonzalo Contreras Aso
Date: 22/09/2022
Summary: Load the already computed real network statistics
         and plot them in a N-E scatter plot with colorbar.
"""

# Import standard data and plotting libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('NetworkStats/real_statistics.csv', index_col = 'Unnamed: 0')
df = df.iloc[::-1]

# Matplotlib parameters
plt.style.use('science')
plt.rcParams["text.usetex"] = False
plt.rcParams['svg.fonttype'] = 'none'

# Initialize figure
plt.figure(figsize = (12,8))
plt.subplot(111)
#plt.title('Comparison between number of nodes and edges,\n and maximum alpha for ranking control\n', fontsize = 20)

# Plot datapoints 
sc = plt.scatter(df['N'], df['E'], c = df['alpha_r_PR'], marker='X', s=150, linewidth=0.5, edgecolor='black', cmap = plt.cm.rainbow) 

# Axis labels and log-log plot
plt.xlabel('Number of nodes', fontsize = 15)
plt.ylabel('Number of edges', fontsize = 15)
plt.yscale('log')
plt.xscale('log')

# Add colorbar
cbar = plt.colorbar(sc)
cbar.set_label('Maximum alpha', rotation=270, fontsize = 15, labelpad=20)

# Save the figure
#plt.tight_layout()
plt.savefig('Figures/Scatter-N-E-alpha.png', transparent=False, facecolor='white')
plt.savefig('Figures/Scatter-N-E-alpha.svg', transparent=False, facecolor='white')

