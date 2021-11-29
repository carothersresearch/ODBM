"""Unit tests for ODBM module"""
import unittest
import numpy as np
from odbm.odbm import *


class Test_ModelBuilder(unittest.TestCase):
    """Unit test for ModelBuilder parent class"""
    def test___init___(self):
        #Test proper initialization of class with proper inputs
        subject = ModelBuilder(species=np.array(['A', 'B', 'C', 'D']),
                                 rxn=np.array(['R1', 'R2', 'R3']),
                                 mech_dict={})
    
        # check to make sure necessary attributes are inputted
        self.assertTrue(subject.species is not None)
        self.assertTrue(subject.species is not None)
        self.assertFalse(subject.mech_dict)
    
    def test_addMechanism(self):
        # test to see if mech_dict dictionary updates with addMechanism
        m = MichaelisMenten
        subject.addMechanism(m)
        self.assertTrue(subject.mech_dict)

    def test_addSpecies(self):
        Label = 'E' 
        StartingConc = '0'
        subject.addSpecies(Label, StartingConc)
        self.assertTrue(subject.species['Label'].str.contains(Label).any())

    def test_addReaction(self):
        mech = 'MA'
        sub = 'A,B'
        prod = 'C'
        param = 'k:100'
        label = 'R4'
        subject.addReaction(Mechanism = mech, Substrate = sub, Product = prod, Parameters = param, Label = label)
        self.assertTrue(subject.rxns['Label'].str.contains(Label).any()))

    def test_writeReaction(self):
        test_str = subject.writeReaction(subject.rxns[subject.rxns['Label']=='R4'])
        # compare what this returns to what we expect? Should we do this for each mechanism type?

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