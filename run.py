import pandas as pd
import tellurium as te
import matplotlib.pyplot as plt
from buildModelFromExcel import initializeValues, writeReactions
import matplotlib.pyplot as plt

model_species = pd.read_excel('model_definition_simple_ex.xlsx', sheet_name = 'Species & Base Mechanisms', engine = 'openpyxl')
model_rxns = pd.read_excel('model_definition_simple_ex.xlsx', sheet_name = 'Reaction', engine = 'openpyxl')

initializeValues(model_species=model_species, model_rxns=model_rxns)
writeReactions(model_rxns)

model = open('model_simple_ex.txt','r').read()
r  = te.loada(model)
s = r.simulate(0,10)
plt.plot(s['time'],s['[ATP]'])
plt.show()
print(r)
