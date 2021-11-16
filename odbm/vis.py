
import pandas as pd
import numpy as np
import tellurium as te
from odbm.odbm import ModelBuilder
import matplotlib.pyplot as plt

def rxn_plot(model:ModelBuilder, sim, rxn_idx = [], figsize = None):
    if figsize is None:
        figsize = (len(model.rxns),3)

    f,ax = plt.subplots(1, len(model.rxns), figsize = figsize)
    for k,r in model.rxns.iterrows():
        if (k in rxn_idx) or (not rxn_idx):
            for j in model.get_substrates(k):
                ax[k].plot(sim['time'],sim['['+j+']'], label = j)
                
            for j in model.get_products(k):
                ax[k].plot(sim['time'],sim['['+j+']'],'--', label = j)  
            ax[k].legend()

    return f, ax