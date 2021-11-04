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
    auto_rxn_str = '\n# Define auto-generated reactions \n'
    auto_rxn_count = 0

    for _, sp in model_species.iterrows():
        label = myformat(sp['Label'], FIND, REPLACE)
        sp['Label'] = label
        
        model_str += (label +'=' + str(sp['Starting Conc']) + '; \n')
        # if its DNA, initialize RNA and protein (AA) to 0
        if 'DNA' in sp['Label']:
            model_str += (label[:-3] +'RNA=0; \n')
            model_str += (label[:-3] +'AA=0; \n')

        if not pd.isnull(sp['Mechanisms']):
            mechanisms = sp['Mechanisms'].split(';')
            for m in mechanisms:
                #auto_rxn_str = writeMechanisms(m,s,auto_rxn_str)
                pass
            pass

    model_str += '\n# Initialize kinetic values \n'
    for _, rxn in model_rxns.iterrows():
        for k in ['K1','K2','K3']:
            if not pd.isnull(rxn[k]):
                #initialize value
                model_str += (k+'_'+rxn['Label'] +'=' + str(rxn[k]) + '; \n')

            # Diego: what about default parameters? say if we want to set all transcription rates to be the same


    with open('model.txt', 'w') as f:
        f.write(model_str)

#add support so either function can be called first - right now initializeValues must be called first, then writeReactions

def writeReactions(model_rxns):
    rxn_str = '\n# Define specified reactions \n'

    fmt = lambda x: myformat(x, FIND, REPLACE) # bettter way of calling this all the time, maybe preprocess all string first?
    for _,rxn in model_rxns.iterrows():
        if rxn['Mechanism'] == 'MA':
            # mass action kinetics
            if str(rxn['Enzyme']) != 'nan':

                for r in rxn['Reactant'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str += fmt(rxn['Enzyme']) + ' -> '
                for p in rxn['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str += fmt(rxn['Enzyme']) + '; '

                rxn_str += 'K1_' + rxn['Label']
                for p in rxn['Reactant'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += '*'+fmt(rxn['Enzyme']) + '; \n'
            else:

                for r in rxn['Reactant'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str = rxn_str[:-3] + ' -> '
                for p in rxn['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str = rxn_str[:-3] + '; '

                rxn_str += 'K1_' + rxn['Label']
                for p in rxn['Reactant'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += ' \n'

        elif rxn['Mechanism'] == 'MM':
            # Michaelis–Menten kinetics
            # must have only one substrate

            N = rxn['Label'] # or ID
            E = rxn['Enzyme']
            if str(E) == 'nan':
                raise NameError('No enzyme specified in Michaelis–Menten mechanism for reaction '+N)

            S = rxn['Reactant'].split(';')
            if len(S)>1:
                raise NameError('More than one substrate specified in Michaelis–Menten mechanism for reaction '+N)
            S = S[0]
            
            P = ' + '.join(map(fmt, rxn['Product'].split(';')))
            rxn_str += fmt(S) + ' + ' + fmt(E) + ' -> ' + fmt(E) + ' + '  + P + '; '
            rxn_str += 'K1_' + N + '*'+fmt(E)+'*'+fmt(S)+'/('+'K2_' + N+' + '+fmt(S)+'); \n'


    with open('model.txt', 'a') as f:
        f.write(rxn_str)
    

                