import pandas as pd
from odbm.utils import extractParams, fmt

from odbm.mechanisms import *
DEFAULT_MECHANISMS = [MichaelisMenten, OrderedBisubstrateBiproduct, MassAction, simplifiedOBB]

class ModelBuilder:

    def __init__(self, species, reactions):
        self.mech_dict = {}
        [self.addMechanism(m) for m in DEFAULT_MECHANISMS]
        self.species = species
        self.rxns = reactions

    def addMechanism(self, new_mechanism):
        self.mech_dict[new_mechanism.name] = new_mechanism

    def writeReaction(self, rxn):
        m = rxn['Mechanism']
        try:
            M = self.mech_dict[m]
            M = M(rxn)
        except KeyError:
            raise KeyError('No mechanism found called '+m)

        rxn_str = '\n'
        rxn_str += M.writeEquation() + M.writeRate()

        return rxn_str
    
    def writeSpecies(self, species):
        label = fmt(species['Label'])
        species['Label'] = label
        
        s_str = (label +'=' + str(species['Starting Conc']) + '; \n')
        # if its DNA, initialize RNA and protein (AA) to 0
        if 'DNA' in species['Label']:
            s_str += (label[:-3] +'RNA=0; \n')
            s_str += (label[:-3] +'AA=0; \n')

        if not pd.isnull(species['Mechanisms']):
            mechanisms = species['Mechanisms'].split(';')
            for m in mechanisms:
                #auto_rxn_str = writeMechanisms(m,s,auto_rxn_str)
                pass
            pass

        return s_str

    def writeParameters(self, rxn):
        p_str = ''
        if not pd.isnull(rxn['Parameters']):
            #initialize value
            kdict = extractParams(rxn['Parameters'])
            for key, value in kdict.items():
                p_str += (key+'_'+rxn['Label'] +'=' + value + '; \n')
        else:
            raise('No parameters found for reaction '+rxn['Label'])
            # Diego: what about default parameters? say if we want to set all transcription rates to be the same

        return p_str

    def compile(self):
        s_str = '# Initialize concentrations \n'
        p_str = '\n# Initialize parameters \n'
        r_str = '# Define specified reactions \n'

        for _, sp in self.species.iterrows():
            s_str += self.writeSpecies(sp)

        for _, rxn in self.rxns.iterrows():
            p_str += self.writeParameters(rxn) + '\n'
            r_str += self.writeReaction(rxn) + '\n'

        return s_str + p_str + r_str

    def saveModel(self, filename):
        with open(filename, 'w') as f:
            f.write(self.compile())

    def get_reaction(self, id):
        if type(id) is int:
            r = self.rxns.iloc[id]
        elif type(id) is str:
            r = self.rxns[self.rxns['Label'] == id]
        return r
    
    def get_substrates(self, id, cofactors = True):
        r = self.get_reaction(id)

        if cofactors and (str(r['Cofactor']) != 'nan'):
            X = [*r['Substrate'].split(';'), *r['Cofactor'].split(';')]
        else:
            X = r['Substrate'].split(';')

        return list(map(fmt, X))

    def get_products(self, id):
        r = self.get_reaction(id)
        return list(map(fmt, r['Product'].split(';')))
