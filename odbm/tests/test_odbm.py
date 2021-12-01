"""Unit tests for ODBM module"""
import unittest
import numpy as np
from odbm.odbm import *


class Test_ModelBuilder(unittest.TestCase):
    """Unit test for ModelBuilder parent class"""
    def test___init___(self):
        #Test proper initialization of class with proper inputs
        self.subject = ModelBuilder(species=np.array(['A', 'B', 'C', 'D']),
                                 rxn=np.array(['R1', 'R2', 'R3']),
                                 mech_dict={})
    
        # check to make sure necessary attributes are inputted
        self.assertTrue(self.subject.species is not None)
        self.assertTrue(self.subject.species is not None)
        self.assertFalse(self.subject.mech_dict)
    
    def test_addMechanism(self):
        # test to see if mech_dict dictionary updates with addMechanism
        m = MichaelisMenten
        self.subject.addMechanism(m)
        self.assertTrue(self.subject.mech_dict)

    def test_addSpecies(self):
        Label = 'E' 
        StartingConc = '0'
        self.subject.addSpecies(Label, StartingConc)
        self.assertTrue(self.subject.species['Label'].str.contains(Label).any())

    def test_addReaction(self):
        mech = 'MA'
        sub = 'A,B'
        prod = 'C'
        param = 'k:100'
        label = 'R4'
        self.subject.addReaction(Mechanism = mech, Substrate = sub, Product = prod, Parameters = param, Label = label)
        self.assertTrue(self.subject.rxns['Label'].str.contains(label).any())

    def test_writeReaction(self):
        test_str = self.subject.writeReaction(self.subject.rxns[self.subject.rxns['Label']=='R4'])
        # compare what this returns to what we expect? Should we do this for each mechanism type?

class Test_ModelHandler(unittest.TestCase):
    def test__init__(self):
        pass

    def test_setBoundarySpecies(self):
        pass

    def test_setConcentrations(self):
        pass

    def test_senstivityAnalysis(self):
        pass

    def test_setSimulationConditions(self):
        pass
    
    def test_run(self):
        pass

    pass