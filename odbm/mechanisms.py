from os import name
from numpy.core.fromnumeric import product
import pandas as pd
import numpy as np
from odbm.utils import extractParams, fmt

class Mechanism:

    # these variables should be overriden in new mechanisms
    name = 'base_mechanism' # name for the mechanism
    required_params = []    # list of required parameters
    nS = 1                  # number of required substrates 
    nP = np.nan             # number of required products, or np.nan
    nE = True               # enzymatic reaction

    def __init__(self,rxn: pd.DataFrame):

        try:
            self.enzyme = rxn['Enzyme']
            self.substrates = rxn['Substrate']
            self.products = rxn['Product']
            self.cofactors = rxn['Cofactor']
            self.params = rxn['Parameters']
            self.label = rxn['Label']
        except:
            raise KeyError("Missing Reaction fields")

        self._processInput()
        self._formatInput()
    
    def _processInput(self):

        # params
        self.params = extractParams(self.params)
        if not np.all([p in self.params for p in self.required_params]):
            raise KeyError("No "+' or '.join(self.required_params)+" found in parameters for reaction "+self.label)

        # cofactor
        if str(self.cofactors) != 'nan':
            self.cofactors = self.cofactors.split(';')
        else:
            self.cofactors = []

        # enzyme
        if (str(self.enzyme) == 'nan') and self.nE:
            raise KeyError('No enzyme specified in reaction '+self.label)

        # substrates
        self.substrates = self.substrates.split(';')
        if len(self.substrates) != self.nS and np.isnan(self.nS) == False:
            raise ValueError(str(len(self.substrates))+' substrate(s) found for a '+ str(self.nS) + ' substrate mechanism in reaction '+self.label)

        # products  
        self.products = self.products.split(';')
        if (not np.isnan(self.nP)) and (len(self.products) != self.nP):
            raise ValueError(str(len(self.products))+' product(s) found for a '+ str(self.nP) + ' product  mechanism in reaction '+self.label)
        
    def _formatInput(self):
        self.products = list(map(fmt, self.products))
        self.substrates = list(map(fmt, self.substrates))
        if (str(self.cofactors) != 'nan'): self.cofactors = list(map(fmt, self.cofactors))
        if (str(self.enzyme) != 'nan'): self.enzyme = fmt(self.enzyme)



    def writeEquation(self) -> str:
        '''
        Writes chemical equations in form of A → B for all reactions defined in dataframe
        Input:
            1. N (str) of Label
            2. P (list) of Products
            3. S (list) of Substrates
            4. E (str) of Enzyme
            5. C (str) of Cofactor

        Returns:
            1. rxn_str (str) of reaction definitions

        Need to fix handling of cofactors here
        They are not involved in rate but should still be balanced in equation
        e.g. I don't want to have to write ATP in substrate and ADP in product 
        but I still need it in equation definition
        '''
        
        allS = ' + '.join([*self.substrates,*self.cofactors])
        allP = ' + '.join(self.products)

        if self.enzyme != 'nan':
            rxn_str = allS + ' + ' + self.enzyme + ' -> ' + self.enzyme + ' + '  + allP
        else: 
            rxn_str = allS + ' -> ' + allP

        return self.label +' : '+rxn_str
    
    def writeRate(self) -> str:
        pass

class MichaelisMenten(Mechanism):
    name = 'MM'                        # name for the mechanism
    required_params = ['kcat','Km']    # list of required parameters
    nS = 1                             # number of required substrates 
    nP = np.nan                        # number of required products 
    nE = True                          # enzymatic reaction
    nC = False

    def writeRate(self) -> str:
        S = self.substrates
        return self.label +' = '+'kcat_' + self.label + '*'+self.enzyme+'*'+S[0]+'/('+'Km_' + self.label+' + '+S[0]+')'
    
class OrderedBisubstrateBiproduct(Mechanism):
    # ordered bisubstrate-biproduct
    # must have two substrates and two products
    # https://iubmb.qmul.ac.uk/kinetics/ek4t6.html#p52
    # looks for kcat, Km1, Km2, K

    name = 'OBB'                                     # name for the mechanism
    required_params = ['kcat', 'Km1', 'Km2', 'K']    # list of required parameters
    nS = 2                                           # number of required substrates 
    nP = 2                                           # number of required products 
    nE = True                                        # enzymatic reaction

    def writeRate(self) -> str:
        S = self.substrates
        N = self.label

        return self.label +' = '+'kcat_' + N + '*'+self.enzyme+'*'+(S[0])+'*'+(S[1])+'/(' \
                    +(S[0])+'*'+(S[1])+'+ Km1_' + N+'*'+(S[0])+'+ Km2_' + N+'*'+(S[1])+'+ K_' + N+')'

class MassAction(Mechanism):
    name = 'MA'                                     # name for the mechanism
    required_params = ['k']                         # list of required parameters
    nS = np.nan                                     # number of required substrates 
    nP = np.nan                                     # number of required products 
    nE = False                                      # enzymatic reaction

    # mass action kinetics
    def writeRate(self) -> str:
        rxn_str = 'k_' + self.label
        for p in self.substrates:
            if p[0].isnumeric():
                p = p[1:]+'^'+p[0]
            rxn_str += '*' + p 
        if self.enzyme != 'nan':
            rxn_str += '*'+(self.enzyme)

        return self.label +' = '+rxn_str

class simplifiedOBB(Mechanism):
    name = 'SOBB'                                     # name for the mechanism
    required_params = ['kcat', 'Km1', 'Km2']    # list of required parameters
    nS = 2                                           # number of required substrates 
    nP = 2                                           # number of required products 
    nE = True                                        # enzymatic reaction

    def writeRate(self) -> str:
        S = self.substrates
        N = self.label

        return self.label +' = '+'kcat_' + N + '*'+self.enzyme+'*'+(S[0])+'*'+(S[1])+'/(' \
                    +(S[0])+'*'+(S[1])+'+ Km1_' + N+'*'+(S[1])+'+ Km2_' + N+'*'+(S[0])+'+ Km1_' + N+ '*Km2_'+ N+')'

# class PI(Mechanism):
class TX_MM(MichaelisMenten):
    name = 'TX_MM'
    required_enzyme = 'RNAP'
    generate_label = lambda l: l+'_TX'
    generate_product = lambda s: s + ';' + s[:-3]+'RNA'

class Modifier(Mechanism):

    name = 'base_modifier'  # name for the mechanism
    required_params = []    # list of required parameters
    nS = 1                  # number of required substrates 
    nP = np.nan             # number of required products, or np.nan
    # nC ???
    nE = True               # enzymatic reaction

    def writeEquation(self):
        # no need 
        pass

    def apply(self, rxn_rate):
        # overide
        pass

class LinearCofactor(Modifier):
    name = 'LC'                                     # name for the mechanism
    required_params = ['maxC']                      # list of required parameters
    nS = np.nan                                     # number of required substrates 
    nP = np.nan                                     # number of required products 
    nE = False                                      # enzymatic reaction

    def apply(self, rxn_rate):
        return rxn_rate+' * ('+self.cofactors[0]+'/maxC_'+self.label+')'
