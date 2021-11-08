from odbm.mechanisms import MA, MM, OBB, PI

DEFAULT_MECHANISMS = [MA,MM,OBB,PI]

class ModelBuilder:

    def __init__(self):
        self.mech_dict = {m.type : m for m in DEFAULT_MECHANISMS}

    def addMechanism(self, new_mechanism):
        self.mech_dict[new_mechanism.type] = new_mechanism

    def writeReaction(self, rxn):
        m = rxn['Mechanism']
        S = rxn['Subsrtates']
        P = rxn['Products']
        try:
            self.mech_dict[m](S, P).writeRate()
        except:
            raise KeyError('No mechanism found called '+m)