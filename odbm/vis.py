
import pandas as pd
import numpy as np
import tellurium as te
from odbm.odbm import ModelBuilder
import matplotlib.pyplot as plt

def rxn_plot(model:ModelBuilder, sim, rxn_idx = [], figsize = None, titles = None):
    if figsize is None:
        figsize = (len(rxn_idx),3)

    f,ax = plt.subplots(1, len(rxn_idx), figsize = figsize, sharey=False)
    for k,r in enumerate(rxn_idx):
        for j in model.get_substrates(r):
            ax[k].plot(sim['time']/60,sim['['+j+']'], label = j)
            
        for j in model.get_products(r):
            ax[k].plot(sim['time']/60,sim['['+j+']'],'--', label = j)

        ax[k].legend()
        if titles: ax[k].set_title(titles[k])

        ax[k].set_xlabel('time (min)')
        ax[k].set_ylabel('Concentraion (mM)')
    f.tight_layout()
    return f, ax