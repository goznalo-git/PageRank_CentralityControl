# Code regarding PageRank centrality control paper

This repository contains the datasets and code used in the numerical analysis on "Can the PageRank centrality be manipulated to obtain any desired ranking?" _Chaos 33, 083152 (2023)_. Here we briefly comment on it.

## How to use

This code is written in Python 3, using standard scientific modules (numpy, matplotlib, scikit-learn, scipy, pandas) as well as a couple of network-theoretic ones (networkx, igraph). The requirements are listed in the `requirements.txt` file, which can be used to create a virtual environment. The code is structured as follows:

- `utilities.py`: script containing most custom functions used in the rest of the executables.
- `real_networks.py`, `synthetic_networks.py`: executables computing different statistics (number of nodes, edges, directedness, alphas and beta) for real and synthetic networks, respectively.
- `figure_scatter_real.py`: executable returning the scatter plot of the maximum alpha for PageRank ranking control in real networks.
- `figure_comparison_biplex_real.py`, `figure_comparison_biplex_synthetic.py`: executables returning the scatter plots comparing the maximum value of the parameters of the standard and biplex PageRank, for real and synthetic networks, respectively.
- `requirements.txt`: Python modules used, can be used to import them in a virtual environment.
- `Datasets`: standardized datasets of real, directed networks used, all in .graphml. Weighted ones are in the DW subfolder, unweighted in the DU subfolder.
- `NetworkStats`: computed statistics are saved here in .csv files. Quadratic fits from the biplex vs standard PageRank figures are also saved here in .txt files.
- `Figures`: the resulting figures are saved in this directory.



**How to cite:** *"Parametric control of PageRank centrality rankings: a geometrical approach"*, Gonzalo Contreras-Aso, Regino Criado, Miguel Romance. To be published.

**Note 1:** in the computation of the maximum alpha available for full centrality control, the algorithm employs a collection of `sample` random centrality vectors (by default, 100). Thus, the obtained values of that parameter in the .csv files might differ every time the code is run, however they should be of the same order.

**Note 2:** The figures obtained are not the final ones presented in the paper. Instead, they are first processed in a vector graphics software (Inkscape) for aesthetic purposes and latex formulae rendering.


All datasets have been scraped from the [KONECT](http://konect.cc/) [1] and the [CASOS](http://www.casos.cs.cmu.edu/) websites.

[1] *KONECT - The Koblenz Network Collection*, Jérôme Kunegis. Proc. Int. Conf. on World Wide Web Companion, 1343--1350 (2013)
