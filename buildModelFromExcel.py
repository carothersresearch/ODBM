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

#add support so either function can be called first - right now initializeValues must be called first, then writeReactions
#maybe make a more intuitive way of having non 1:1 stoichiometries - right now if A -> 2B, excel wants B, B in "Product" column
def writeReactions():
    rxn_str = '\n #Define reactions \n'
    for rxn in model_rxns.iterrows():
        if rxn[1]['Mechanism'] == 'MA':
            if str(rxn[1]['Enzyme']) != 'nan':
                # mass action kinetics
                for r in rxn[1]['Reactant'].split(','):
                    rxn_str += r + ' +'
                rxn_str = rxn_str[:-2] + ' + ' + rxn[1]['Enzyme'] + ' -> '
                for p in rxn[1]['Product'].split(','):
                    rxn_str += p + ' +'
                rxn_str = rxn_str[:-2] + ' + ' + rxn[1]['Enzyme'] + '; '   
                rxn_str += 'K1_' + rxn[1]['Label']
                for p in rxn[1]['Product'].split(','):
                    rxn_str += '*' + p 
                rxn_str += ' \n'
            else:
                for r in rxn[1]['Reactant'].split(','):
                    rxn_str += r + ' +'
                rxn_str = rxn_str[:-2] + ' -> '
                for p in rxn[1]['Product'].split(','):
                    rxn_str += p + ' +'
                rxn_str = rxn_str[:-2] + '; '
                rxn_str += 'K1_' + rxn[1]['Label']
                for p in rxn[1]['Product'].split(','):
                    rxn_str += '*' + p 
                rxn_str += ' \n'
    with open('model.txt', 'a') as f:
    f.write(rxn_str)
    

                