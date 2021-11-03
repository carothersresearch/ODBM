import pandas as pd
import numpy as np
import tellurium as te
from buildModelFromExcel import initializeValues, writeReactions

model_species = pd.read_excel('model_definition.xlsx', sheet_name = 'Species', engine = 'openpyxl')
model_rxns = pd.read_excel('model_definition.xlsx', sheet_name = 'Reaction', engine = 'openpyxl')

initializeValues(model_species=model_species, model_rxns=model_rxns)
writeReactions(model_rxns)

model = open('model.txt','r').read()
r  = te.loada(model)
print(r)