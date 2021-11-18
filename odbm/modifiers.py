from overrides import overrides, final
from odbm.odbm import Mechanism
import numpy as np

class Modifier(Mechanism):
    """
    A superclass class used to handle basic Mechansim modification functionality. Inherits from Mechanism.
    Other mechanism should inherint this class and override attributes and apply(rxn_rate)

    Attributes
    ----------
    name : str
        label used to identify mechanism
    required_params : list
        list with parameter strings, default []
    nS : int
        number of required substrates, default np.nan
    nC : int
        number of required cofactors, default np.nan
    nP : int
        number of required products, default np.nan
    nE : int
        number of required enzymes, default np.nan

    Methods
    -------
    apply(rxn_rate: str):
        Apply modification to reaction rate string

    """

    name = 'base_modifier'  # name for the mechanism
    required_params = []    # list of required parameters

    @overrides
    @final
    def writeEquation(self) -> str:
        return

    def apply(self, rxn_rate: str) -> str:
        """
        Apply modification to reaction rate string

        Parameters
        ----------
        rxn_rate : str
            Original reaction rate

        Returns
        -------
        str
            Modified reaction rate
        """
        return

class LinearCofactor(Modifier):

    name = 'LC'                                     
    required_params = ['maxC']                     
    nC = 1

    @overrides
    def apply(self, rxn_rate) -> str:
        return rxn_rate+' * ('+self.cofactors[0]+'/maxC_'+self.label+')'
