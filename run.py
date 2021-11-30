import pandas as pd
import tellurium as te
from buildModelFromExcel import initializeValues, writeReactions
from odbm.odbm import ModelBuilder

#file_path = input('File path to model definition (excel format):')

#Define DataFrames of species, reactions from input model
model_species = pd.read_excel('Examples/multi_enzyme_model.xlsx', sheet_name = 'Species & Base Mechanisms', engine = 'openpyxl').dropna('index','all')
model_rxns = pd.read_excel('Examples/multi_enzyme_model.xlsx', sheet_name = 'Reaction', engine = 'openpyxl').dropna('index','all')

#Generate and save model to txt file
modelfile = 'Examples/multi_enzyme_model.txt'
myModel = ModelBuilder(model_species, model_rxns)
myModel.saveModel(modelfile)

#Run simulation
model = open(modelfile,'r').read()
r  = te.loada(model)
s = r.simulate(0,10)


#Write simulation results to excel sheet
#sim_df = pd.DataFrame(s, columns = s.colnames).round(2)
#sim_df.to_csv('Examples/model_txtl_test.xlsx', sheet_name = 'Results')

