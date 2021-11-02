import pandas as pd

model_species = pd.read_excel('C:/Users/rycar/Desktop/UW/BIOEN 537/model_definition_BIOEN537.xlsx', sheet_name = 'Species')
model_rxns = pd.read_excel('C:/Users/rycar/Desktop/UW/BIOEN 537/model_definition_BIOEN537.xlsx', sheet_name = 'Reaction')

#initializes model with starting concentrations for each species and kinetic values, writes to text file
def initializeValues(model_species, model_rxns):

    model_str = ''
    model_str += '#Initialize concentrations \n'
    for sp in model_species.iterrows():
        model_str += (sp[1]['Label'] +'=' + str(sp[1]['Starting Conc']) + '; \n')
        
    model_str += '\n#Initialize kinetic values \n'
    for rxn in model_rxns.iterrows():
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K1']):
            #initialize value
            model_str += ('K1_'+rxn[1]['Label'] +'=' + str(rxn[1]['K1']) + '; \n')
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K2']):
            model_str += ('K2_'+rxn[1]['Label'] +'=' + str(rxn[1]['K2']) + '; \n')
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K2']):
            model_str += ('K3_'+rxn[1]['Label'] +'=' + str(rxn[1]['K3']) + '; \n')

    with open('model.txt', 'w') as f:
        f.write(model_str)


def writeReactions():
    