import pandas as pd
import tellurium as te
import matplotlib.pyplot as plt
from buildModelFromExcel import initializeValues, writeReactions
import matplotlib.pyplot as plt

from odbm.odbm import ModelBuilder

model_species = pd.read_excel('model_txtl_test.xlsx', sheet_name = 'Species & Base Mechanisms', engine = 'openpyxl')
model_rxns = pd.read_excel('model_txtl_test.xlsx', sheet_name = 'Reaction', engine = 'openpyxl')

modelfile = 'txtl_model.txt'
myModel = ModelBuilder(model_species, model_rxns)
myModel.saveModel(modelfile)

model = open(modelfile,'r').read()
r  = te.loada(model)
s = r.simulate(0,10)
