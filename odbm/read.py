import pandas as pd
from biocrnpyler import Metabolite, Enzyme

def read_model_info(file):
    # TODO: check file is the right format

    return pd.read_excel(file,engine='openpyxl', sheet_name = None)

lol = read_model_info('model_definition.xlsx')
print(lol)

def create_species_reactions(model_def:dict):

    for sheet, df in model_def:
        if sheet == 'Species':
            pass
        elif sheet == 'Reaction':
            pass
        else:
            raise KeyError("Don't know how to handle "+sheet)

    pass
