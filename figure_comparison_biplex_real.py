"""
Author: Gonzalo Contreras Aso
Date: 21/09/2022
Summary: Load the data corresponding to real networks
         and plot datapoints with ranking alpha against
         ranking beta. Adjust a quadratic polynomial.
"""

# Import standard data and plotting libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load the data
df = pd.read_csv('NetworkStats/real_statistics.csv', index_col = 'Unnamed: 0')
df = df.iloc[::-1]

# Fit a quadric polynomial to the data
y = df['alpha_r_PR']
x = df['beta_r_BPR']

model = np.poly1d(np.polyfit(x, y, 2))
print(model)
with open('NetworkStats/fit_real.txt', 'w') as f:
    f.write(str(model))

# Matplotlib parameters
plt.style.use('science')
plt.rcParams["text.usetex"] = False
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['font.serif'] = "CMU Serif"

# Initialize the figure
plt.figure(figsize = (12,8))
#plt.title('Comparison between standard and biplex PageRank parameters\n', fontsize=18)
plt.xlabel('maximum beta', fontsize=15)
plt.ylabel('maximum alpha', fontsize=15)
plt.xlim(0,1)
plt.ylim(0,1)

# Datapoints
plt.scatter(df[df['Weighted?'] == True]['beta_r_BPR'], df[df['Weighted?'] == True]['alpha_r_PR'], color='blue', alpha=0.4, s=80)
plt.scatter(df[df['Weighted?'] == False]['beta_r_BPR'], df[df['Weighted?'] == False]['alpha_r_PR'], color='red', alpha=0.4, s=80)

# y = x line
plt.plot(np.linspace(0,1,100), np.linspace(0,1,100), color='grey', alpha=0.4, linestyle=(0, (10, 10)))

# Polynomial regression
polyline = np.linspace(0,1,100)
plt.plot(polyline, model(polyline), color='green', linewidth=1)

# Custom legend
custom_dots = [Line2D([], [], marker='o', linestyle='None', markersize=10, color='blue', alpha=0.4),
                Line2D([], [], marker='o', linestyle='None', markersize=10, color='red', alpha=0.4),
                Line2D([], [], linestyle=(0, (10, 10)), color='grey', alpha=0.4),
                Line2D([], [], linestyle='-', color='green', linewidth=1)]

plt.legend(custom_dots, ['Weighted', 'Unweighted', 'alpha = beta', 'Quadratic fit: alpha = 1.014 beta^2 + 0.492 beta - 0.041'], fontsize=13)

# Save the figure
#plt.tight_layout()
plt.savefig('Figures/BPRvsPR_alphas.png', facecolor='white', transparent=False)
plt.savefig('Figures/BPRvsPR_alphas.svg', facecolor='white', transparent=False)


