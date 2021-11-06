import pandas as pd
import numpy as np

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

def str_2_dict(mystr):
    mydict = {}
    mystr = mystr.split(';')
    for s in mystr:
        k,v = s.split(':')
        mydict[k.strip()] = v.strip()
    return mydict


###Ryan: to write
def extractParams(params):
    #split key/dict pairs by semicolon and key/dict by colon
    #return dict

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
        if not pd.isnull(rxn['Parameters']):
            #initialize value
            kdict = str_2_dict(rxn['Parameters'])
            for key, value in kdict.items():
                model_str += (key+'_'+rxn['Label'] +'=' + value + '; \n')
        else:
            raise('No parameteres found for reaction '+rxn['Label'])
            # Diego: what about default parameters? say if we want to set all transcription rates to be the same


    with open('model.txt', 'w') as f:
        f.write(model_str)

#add support so either function can be called first - right now initializeValues must be called first, then writeReactions

def writeReactions(model_rxns):
    """"
    kjghlhjgjh
    """
    rxn_str = '\n# Define specified reactions \n'

    fmt = lambda x: myformat(x, FIND, REPLACE) # bettter way of calling this all the time, maybe preprocess all string first?
    for _,rxn in model_rxns.iterrows():

        # cofactor
        C = rxn['Cofactor']
        if str(C) != 'nan':
            C = C.split(';')
        else:
            C = []
        
        params = extractParams(rxn['Parameters'])
        ### Ryan: added code here to try to create mechanism object, not sure if this right 
        #mechanism = Mechanism(type = rxn['Mechanism'], reactant = rxn['Substrate'], 
         #           enzyme = rxn['Enzyme'], product = rxn['Product'], params = params)
         # call mechanism.WriteEquation()
       
       
        if rxn['Mechanism'] == 'MA':
            # mass action kinetics
            if str(rxn['Enzyme']) != 'nan':

                for r in rxn['Substrate'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str += fmt(rxn['Enzyme']) + ' -> '
                for p in rxn['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str += fmt(rxn['Enzyme']) + '; '

                rxn_str += 'K1_' + rxn['Label']
                for p in rxn['Substrate'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += '*'+fmt(rxn['Enzyme']) + '; \n'
            else:

                for r in rxn['Substrate'].split(';'):
                    rxn_str += fmt(r) + ' + '
                rxn_str = rxn_str[:-3] + ' -> '
                for p in rxn['Product'].split(';'):
                    rxn_str += fmt(p) + ' + '
                rxn_str = rxn_str[:-3] + '; '

                rxn_str += 'K1_' + rxn['Label']
                for p in rxn['Substrate'].split(';'):
                    p = fmt(p)
                    if p[0].isnumeric():
                        p = p[1:]+'^'+p[0]
                    rxn_str += '*' + p 
                rxn_str += ' \n'

        elif rxn['Mechanism'] == 'MM':
            # Michaelis–Menten kinetics
            # must have only one substrate
            # looks for kcat and Km

            
            N = rxn['Label'] # or ID

            E = rxn['Enzyme']
            if str(E) == 'nan':
                raise KeyError('No enzyme specified in reaction '+N)

            S = rxn['Substrate'].split(';')
            if len(S)>1:
                raise ValueError('More than one substrate specified in Michaelis–Menten mechanism for reaction '+N)

            params = ['kcat','Km']
            if not np.all([p in str_2_dict(rxn['Parameters']) for p in params]):
                raise KeyError("No "+' or '.join(params)+" found in parameters for reaction "+N)

            allS = ' + '.join(map(fmt, [*S,*C]))
            allP = ' + '.join(map(fmt, rxn['Product'].split(';')))

            rxn_str += fmt(allS) + ' + ' + fmt(E) + ' -> ' + fmt(E) + ' + '  + allP + '; '
            rxn_str += 'kcat_' + N + '*'+fmt(E)+'*'+fmt(*S)+'/('+'Km_' + N+' + '+fmt(*S)+'); \n'

        elif rxn['Mechanism'] == 'OBB':
            # ordered bisubstrate-biproduct
            # must have two substrates and two products
            # https://iubmb.qmul.ac.uk/kinetics/ek4t6.html#p52
            # looks for kcat, Km1, Km2, K

            N = rxn['Label'] # or ID
            
            E = rxn['Enzyme']
            if str(E) == 'nan':
                raise KeyError('No enzyme specified in reaction '+N)

            S = rxn['Substrate'].split(';')
            if len(S) != 2:
                raise ValueError(str(len(S))+'substrate(s) found for a bisubstrate mechanism in reaction '+N)

            P = rxn['Product'].split(';')
            if len(S) != 2:
                raise ValueError(str(len(P))+'product(s) found for a biproduct mechanism in reaction '+N)
                
            params = ['kcat', 'Km1', 'Km2', 'K']
            if not np.all([p in str_2_dict(rxn['Parameters']) for p in params]):
                raise KeyError("No "+' or '.join(params)+" found in parameters for reaction "+N) 

            allS = ' + '.join(map(fmt, [*S,*C]))
            allP = ' + '.join(map(fmt, P))

            rxn_str += allS + ' + ' + fmt(E) + ' -> ' + fmt(E) + ' + '  + allP + '; '
            rxn_str += 'kcat_' + N + '*'+fmt(E)+'*'+fmt(S[0])+'*'+fmt(S[1])+'/(' \
                         +fmt(S[0])+'*'+fmt(S[1])+'+ Km1_' + N+'*'+fmt(S[0])+'+ Km2_' + N+'*'+fmt(S[1])+'+ K_' + N+'); \n'

    with open('model.txt', 'a') as f:
        f.write(rxn_str)
    

            