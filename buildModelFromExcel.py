import pandas as pd

def myformat(x, find, replace):
    x = x.upper()
    if x[0].isnumeric() and x[1] != ' ':
        x = 'z'+x 
    for f,r in zip(find,replace):
        x = x.replace(f,r)
    x = x.strip()
    return x

FIND = ['-',',','+',' ']
REPLACE = ['_','_','_plus','']

#initializes model with starting concentrations for each species and kinetic values, writes to text file
def initializeValues(model_species, model_rxns):

    model_str = '# Initialize concentrations \n'
    for sp in model_species.iterrows():
        label = myformat(sp[1]['Label'], FIND, REPLACE)
        sp[1]['Label'] = label
        
        model_str += (label +'=' + str(sp[1]['Starting Conc']) + '; \n')
        # if its DNA, initialize RNA and protein (AA) to 0
        if 'DNA' in sp[1]['Label']:
            model_str += (label[:-3] +'RNA=0; \n')
            model_str += (label[:-3] +'AA=0; \n')

    model_str += '\n# Initialize kinetic values \n'
    for rxn in model_rxns.iterrows():
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K1']):
            #initialize value
            model_str += ('K1_'+rxn[1]['Label'] +'=' + str(rxn[1]['K1']) + '; \n')
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K2']):
            model_str += ('K2_'+rxn[1]['Label'] +'=' + str(rxn[1]['K2']) + '; \n')
        if not pd.isnull(model_rxns.iloc[rxn[0]]['K3']):
            model_str += ('K3_'+rxn[1]['Label'] +'=' + str(rxn[1]['K3']) + '; \n')

            # Diego: what about default parameters? say if we want to set all transcription rates to be the same

    with open('model.txt', 'w') as f:
        f.write(model_str)

#add support so either function can be called first - right now initializeValues must be called first, then writeReactions
#maybe make a more intuitive way of having non 1:1 stoichiometries - right now if A -> 2B, excel wants B, B in "Product" column
    # Diego: why is that the case? what happens if you put "[...], 3 NADH, [...]" in excel?

def writeReactions(model_rxns):
    rxn_str = '\n# Define specified reactions \n'
    auto_rxn_str = '\n# Define auto-generated reactions \n'
    auto_rxn_count = 0

    fmt = lambda x: myformat(x, FIND, REPLACE)
    for rxn in model_rxns.iterrows():
        if rxn[1]['Mechanism'] == 'MA':
            if str(rxn[1]['Enzyme']) != 'nan':
                # mass action kinetics

                for r in rxn[1]['Reactant'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str += fmt(rxn[1]['Enzyme']) + ' -> '
                for p in rxn[1]['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str += fmt(rxn[1]['Enzyme']) + '; '

                rxn_str += 'K1_' + rxn[1]['Label']
                for p in rxn[1]['Reactant'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += '*'+fmt(rxn[1]['Enzyme']) + '; \n'
            else:

                for r in rxn[1]['Reactant'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str = rxn_str[:-3] + ' -> '
                for p in rxn[1]['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str = rxn_str[:-3] + '; '

                rxn_str += 'K1_' + rxn[1]['Label']
                for p in rxn[1]['Reactant'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += ' \n'

        elif rxn[1]['Mechanism'] == 'TX':
            pass

    with open('model.txt', 'a') as f:
        f.write(rxn_str)
    

                