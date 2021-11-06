import pandas as pd
import numpy as np

class Mechanism:
    type = self.type
    reactant = self.reactant
    enzyme = self.enzyme
    product = self.product
    params = self.params
    
    rxn_str = '\n# Define specified reactions \n'
    def writeEquation(product, reactant, enzyme):
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

    
    if type == 'MM':
        self.MM(reactant, enzyme, product, params)
    elif type = 'OBB':
        self.OBB(reactant, enzyme, product, params)
    elif type = 'MA':
        self.MA(reactant, enzyme, product, params)
    elif type = 'PI':
        self.PI(reactant, enzyme, product, params)


class MM(Mechanism):
           

class OBB(Mechanism):


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


