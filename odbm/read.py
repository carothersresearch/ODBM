import pandas as pd
from biocrnpyler import Metabolite, Enzyme

def read_model_info(file):
    # TODO: check file is the right format

    return pd.read_excel(file,engine='openpyxl', sheet_name = None)



def create_species_reactions(model_def:dict):
    components = []
    for sheet, df in model_def.items():
        if sheet == 'Species':
            pass
        elif sheet == 'Reaction':
            def myformat(x, F, R):
                    for f,r in zip(F,R):
                        x = x.replace(f,r)
                    x = x.strip()
                    x = x.upper()
                    if x[0].isnumeric():
                        x = 'z'+x 
                    return x
            F = ['-',',','+',' ']
            R = ['_','_','_plus','']

            for i in range(len(df)):

                substrates = [myformat(x,F,R) for x in df.iloc[i]['Reactant'].split(';')]
                products = [myformat(x,F,R) for x in df.iloc[i]['Product'].split(';')]
                enzyme = df.iloc[i]['Enzyme'].strip().upper()
                mechanism = df.iloc[i]['Mechanism']

                E = Enzyme(enzyme, substrates, products, mechanisms = mechanism)
                
                components.append(E)

            pass
        else:
            raise KeyError("Don't know how to handle "+sheet)

    pass

lol = create_species_reactions(read_model_info('model_definition.xlsx'))
print(lol)