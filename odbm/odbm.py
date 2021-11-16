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
            # bug here: throws error for no mechanism found even if issue is incorrect parameters
            raise KeyError('No mechanism found called '+m)

        rxn_str = '\n'
        rxn_str += M.writeEquation() + M.writeRate()

        return rxn_str


    def addTranscription(self, species):
        #Not sure what best way to define default txn rate is
        #Promoter strength can be programmed in through k1

        default_tx = 10 
        TX = {}
        TX['Label'] = fmt(species['Label']) + "_TX"
        TX['Substrate'] = species['Label']
        TX['Product'] = (species['Label'][:-3] +'RNA')

        if 'TX1' in species['Mechanisms']:
            TX['Enzyme'] = 'RNAP'
            TX['Mechanism'] = 'MA'
            if not pd.isnull(species['K1']):
                TX['Parameters'] = 'k:'+str(species['K1'])
            else:
                TX['Parameters'] = 'k:'+str(default_tx)
            
        
        if 'CRISPRa' in species['Mechanisms']:
            TX['Enzyme'] = 'RNAP,dCas9,MCP-SoxS'
            TX['Mechanism'] = 'CRISPR'
            TX['Parameters'] = 'k:'+str(default_tx)

        return TX

    def addTranslation(self, species):
        default_tl = 10 #Not sure what best way to define default txn rate is
        TL = {}
        TL['Label'] = fmt(species['Label']) + "_TL"
        TL['Substrate'] = species['Label'][:-3] +'RNA'
        TL['Product'] = (species['Label'][:-4])
        TL['Enzyme'] = 'Ribosome'
        # we may want to change the mechanism
        TL['Mechanism'] = 'MA' 
        if not pd.isnull(species['K2']):
            TL['Parameters'] = 'k:'+str(species['K2'])
        else:
            TL['Parameters'] = 'k:'+str(default_tl)
        
        return TL


    def writeSpecies(self, species):
        label = fmt(species['Label'])
        species['Label'] = label
        
        s_str = (label +'=' + str(species['Starting Conc']) + '; \n')
        # if its DNA, initialize RNA and protein (AA) to 0
        if 'DNA' in species['Label']:
            s_str += (label[:-3] +'RNA=0; \n') #RNA
            self.rxns = self.rxns.append(self.addTranscription(species), ignore_index = 'True')

            s_str += (label[:-4] +'=0; \n') #Enzyme
            self.rxns = self.rxns.append(self.addTranslation(species), ignore_index = 'True')


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
                p_str += (key+'_'+rxn['Label'] +'=' + str(value) + '; \n')
        else:
            raise('No parameters found for reaction '+rxn['Label'])
            # Diego: what about default parameters? say if we want to set all transcription rates to be the same

        return p_str


    def compile(self):
        s_str = '# Initialize concentrations \n'
        p_str = '\n# Initialize parameters \n'
        r_str = '# Define specified reactions \n'

        if 'DNA' in self.species['Type']:
            #how to add species?
            self.species = self.species.append({'Label':'Ribosome', 'Starting Conc':1, 'Type':'Enzyme'}, ignore_index =True)
            self.species = self.species.append({'Label':'RNAP', 'Starting Conc':1, 'Type':'Enzyme'}, ignore_index = True)

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
