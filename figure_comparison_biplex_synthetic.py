"""
Author: Gonzalo Contreras Aso
Date: 21/09/2022
Summary: Load the data corresponding to synthetic networks
         and plot datapoints with ranking alpha against
         ranking beta. Adjust a quadratic polynomial.
"""

# Import standard data and plotting libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# Load the data
df = pd.read_csv('NetworkStats/synthetic_statistics.csv', index_col = 'Unnamed: 0')
df = df.iloc[::-1]

# Fit a quadric polynomial to the data
y = df['alpha_r_PR']
x = df['beta_r_BPR']

model = np.poly1d(np.polyfit(x, y, 2))
print(model)
with open('NetworkStats/fit_synthetic.txt', 'w') as f:
    f.write(str(model))

# Matplotlib parameters
plt.style.use('science')
plt.rcParams["text.usetex"] = False
plt.rcParams['svg.fonttype'] = 'none'

# Initialize the figure
plt.figure(figsize = (12,8))
#plt.title('Comparison between standard and biplex PageRank parameters\n', fontsize=18)
plt.xlabel('maximum beta', fontsize=15)
plt.ylabel('maximum alpha', fontsize=15)
plt.xlim(0,1)
plt.ylim(0,1)

# Datapoints
plt.scatter(df[df['Type'] == 'ScaleFree']['beta_r_BPR'], df[df['Type'] == 'ScaleFree']['alpha_r_PR'], color='blue', alpha=0.4, s=80)
plt.scatter(df[df['Type'] == 'Random']['beta_r_BPR'], df[df['Type'] == 'Random']['alpha_r_PR'], color='red', alpha=0.4, s=80)

# y = x line
plt.plot(np.linspace(0,1,100),np.linspace(0,1,100), color='grey', alpha=0.4, linestyle=(0, (10, 10)))

# Polynomial regression
polyline = np.linspace(0,1,100)
plt.plot(polyline, model(polyline), color='green', linewidth=1)

# Custom legend
custom_dots = [Line2D([], [], marker='o', linestyle='None', markersize=10, color='blue', alpha=0.4),
                Line2D([], [], marker='o', linestyle='None', markersize=10, color='red', alpha=0.4),
                Line2D([], [], linestyle=(0, (10, 10)), color='grey', alpha=0.4),
                Line2D([], [], linestyle='-', color='green', linewidth=1)]

plt.legend(custom_dots, ['Directed scale-free', 'Directed random', 'alpha = beta', 'Quadratic fit alpha = 1.138 beta^2 + 0.382 beta - 0.016'], fontsize=13, loc="lower right")

## Zoomed-in figure ##
ax = plt.gca()
axzoom = zoomed_inset_axes(ax, 3, loc='upper left')

# Zoomed-in datapoints
plt.scatter(df[df['Type'] == 'ScaleFree']['beta_r_BPR'], df[df['Type'] == 'ScaleFree']['alpha_r_PR'], color='blue', alpha=0.4, s=80)
plt.plot(polyline, model(polyline), color='green', linewidth=1)
plt.plot(np.linspace(0,1,100),np.linspace(0,1,100), color='grey', alpha=0.4, linestyle=(0, (10, 10)))

# Zoomed-in config
axzoom.set_xlim(0, 0.1)
axzoom.set_ylim(0, 0.1)
plt.xticks(visible=False)
plt.yticks(visible=False)
mark_inset(ax, axzoom, loc1=2, loc2=4, fc="none", ec="0.5")

# Save the figure
#plt.tight_layout()
plt.savefig('Figures/BPRvsPR_synth_alphas.png', facecolor='white', transparent=False)
plt.savefig('Figures/BPRvsPR_synth_alphas.svg', facecolor='white', transparent=False)

