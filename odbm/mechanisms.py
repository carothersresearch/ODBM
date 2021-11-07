import pandas as pd
import numpy as np

class Mechanism:

    def __init__(self, type, reactant,enzyme, product, cofactor, params):
        self.type = type
        self.reactant = reactant
        self.enzyme = enzyme
        self.product = product
        self.cofactor = cofactor
        self.params = params
    
    def handleCofactor(cofactor):
        # only handles common cofactors (ATP, NADH) and not very well
        # The idea I'm going for is we read in the cofactor 
        # and can return the substrate/product form to be used for writing the equation
        if cofactor == 'ATP':
            C = ['ATP','ADP']
        elif cofactor == 'NADH':
            C = ['NADH', 'NAD_plus']
        return C


    rxn_str = '\n# Define specified reactions \n'
    def writeEquation(product, reactant, enzyme, cofactor):
        '''
        Need to fix handling of cofactors here
        They are not involved in rate but should still be balanced in equation
        e.g. I don't want to have to write ATP in substrate and ADP in product 
        but I still need it in equation definition
        '''
        #N = rxn['Label'] # or ID
        #E = rxn['Enzyme']
        #S = rxn['Substrate'].split(';')
        #P = rxn['Product'].split(';')
        #C = handleCofactor(cofactor)

        if enzyme != 'nan':
            for r in reactant.split(';'):
                rxn_str += fmt(r) + ' + '
            rxn_str += fmt(enzyme) + ' -> '
            for p in product.split(';'):
                rxn_str += fmt(p) + ' + '
            rxn_str += fmt(enzyme) + '; '
        else:
            for r in rxn['Substrate'].split(';'):
                rxn_str += fmt(r) + ' + '
            rxn_str = rxn_str[:-3] + ' -> '
            for p in rxn['Product'].split(';'):
                rxn_str += fmt(p) + ' + '
            rxn_str = rxn_str[:-3] + '; '


        '''
        allS = ' + '.join(map(fmt, [*S,*C[0]]))
        allP = ' + '.join(map(fmt, [*P, *C[1]])
        if E != 'nan':
            rxn_str += fmt(allS) + ' + ' + fmt(E) + ' -> ' + fmt(E) + ' + '  + allP + '; '
        else: 
            rxn_str += fmt(allS) + ' -> ' allP + '; '

        '''

    #how to call custom mechanism?
        # mech = str(type)
        # self.mech()

    #Ryan: this is the part where I'm confused - how to properly make a class within class. 
    if type == 'MM':
        self.MM(reactant, enzyme, product, params)
    elif type = 'OBB':
        self.OBB(reactant, enzyme, product, params)
    elif type = 'MA':
        self.MA(reactant, enzyme, product, params)
    elif type = 'PI':
        self.PI(reactant, enzyme, product, params)


class MM(Mechanism):
    def writeRate:
        N = rxn['Label'] # or ID
        if str(E) == 'nan':
            raise KeyError('No enzyme specified in reaction '+N)

        if len(S)>1:
            raise ValueError('More than one substrate specified in Michaelis–Menten mechanism for reaction '+N)

        params = ['kcat','Km']
        if not np.all([p in extractParams(rxn['Parameters']) for p in params]):
            raise KeyError("No "+' or '.join(params)+" found in parameters for reaction "+N)

        # Want to have general function that writes the equation and use this to write the rate
        #writeEquation(product, reactant, enzyme, cofactor)
        rxn_str += 'kcat_' + N + '*'+fmt(E)+'*'+fmt(*S)+'/('+'Km_' + N+' + '+fmt(*S)+'); \n'
    

class OBB(Mechanism):
    # ordered bisubstrate-biproduct
    # must have two substrates and two products
    # https://iubmb.qmul.ac.uk/kinetics/ek4t6.html#p52
    # looks for kcat, Km1, Km2, K

    N = rxn['Label'] # or ID

    if str(E) == 'nan':
        raise KeyError('No enzyme specified in reaction '+N)

    if len(S) != 2:
        raise ValueError(str(len(S))+'substrate(s) found for a bisubstrate mechanism in reaction '+N)

    if len(P) != 2:
        raise ValueError(str(len(P))+'product(s) found for a biproduct mechanism in reaction '+N)
        
    params = ['kcat', 'Km1', 'Km2', 'K']
    if not np.all([p in p for p in params]):
        raise KeyError("No "+' or '.join(params)+" found in parameters for reaction "+N) 

    # Want to have general function that writes the equation and use this to write the rate
    #writeEquation(product, reactant, enzyme, cofactor)
    rxn_str += 'kcat_' + N + '*'+fmt(E)+'*'+fmt(S[0])+'*'+fmt(S[1])+'/(' \
                    +fmt(S[0])+'*'+fmt(S[1])+'+ Km1_' + N+'*'+fmt(S[0])+'+ Km2_' + N+'*'+fmt(S[1])+'+ K_' + N+'); \n'



class MA(Mechanism):
 # mass action kinetics
    def writeRate:
        rxn_str += 'K1_' + rxn['Label']
        for p in rxn['Substrate'].split(';'):
            p = fmt(p)
            if p[0].isnumeric():
                p = p[1:]+'^'+p[0]
            rxn_str += '*' + p 
        if enzyme != 'nan':
            rxn_str += '*'+fmt(enzyme) + '; \n'
        else:
            rxn_str += ' \n'  

  
class PI(Mechanism):


