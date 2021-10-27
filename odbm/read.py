import pandas as pd
from biocrnpyler import Metabolite, Reaction, BasicCatalysis, Mixture, Species,HillPositive,ChemicalReactionNetwork

def read_model_info(file):
    # TODO: check file is the right format

    return pd.read_excel(file,engine='openpyxl', sheet_name = None)



def create_species_reactions(model_def:dict):

    def myformat(x, find, replace):
        for f,r in zip(find,replace):
            x = x.replace(f,r)
        x = x.strip()
        x = x.upper()
        if x[0].isnumeric():
            x = 'z'+x 
        return x
    find = ['-',',','+',' ']
    replace = ['_','_','_plus','']

    for sheet, df in model_def.items():
        if sheet == 'Species':
            species = {myformat(i,find,replace):Species(myformat(i,find,replace)) for i in df['Label']}
            
        elif sheet == 'Reaction':
            reactions = []

            for i in range(len(df)):
                enzyme = myformat(df.iloc[i]['Enzyme'],find,replace)
                substrates = [*[myformat(x,find,replace) for x in df.iloc[i]['Reactant'].split(';')], enzyme]
                products = [*[myformat(x,find,replace) for x in df.iloc[i]['Product'].split(';')], enzyme]

                substrates = [species[x] for x in substrates]
                products = [species[x] for x in products]
                mechanism = df.iloc[i]['Mechanism']

                hill_neg  = HillPositive(k=1, s1=substrates[0], K=5, n=2) # just for testing
                R = Reaction(substrates, products, propensity_type=hill_neg)
                
                reactions.append(R)

            pass
        else:
            raise KeyError("Don't know how to handle "+sheet)

    return species, reactions

species, reactions = create_species_reactions(read_model_info('model_definition.xlsx'))
CRN = ChemicalReactionNetwork(list(species.values()), reactions)
CRN.pretty_print(show_rates = True, show_attributes = False, show_materials = True, show_keys = False)
