from biocrnpyler import ChemicalReactionNetwork as CRN
from typing import Dict, List, Tuple, Union
import libsbml
from warnings import warn

class DCRN(CRN):

    def simulate_with_roadrunner(self, timepoints: List[float], initial_condition_dict: Dict[str,float]=None, return_roadrunner=False, check_validity=True):
        """To simulate using roadrunner.
        Arguments:
        timepoints: The array of time points to run the simulation for.
        initial_condition_dict:
        Returns the results array as returned by RoadRunner OR a Roadrunner model object.
        Refer to the libRoadRunner simulator library documentation 
        for details on simulation results: (http://libroadrunner.org/)[http://libroadrunner.org/]
        NOTE : Needs roadrunner package installed to simulate.
        """
        res_ar = None
        try:
            import roadrunner
            import io
            document, _ = self.generate_sbml_model(stochastic_model=False, check_validity=check_validity)
            sbml_string = libsbml.writeSBMLToString(document)
            # write the sbml_string into a temporary file in memory instead of a file
            string_out = io.StringIO()
            string_out.write(sbml_string)
            # use the temporary file in memory to load the model into libroadrunner
            rr = roadrunner.RoadRunner(string_out.getvalue())
            if initial_condition_dict:
                for species, value in initial_condition_dict.items():
                    rr.model[f"init([{species}])"] = value

            if return_roadrunner:
                return rr
            else:
                result = rr.simulate(timepoints[0], timepoints[-1], len(timepoints))
                res_ar = result
        except ModuleNotFoundError:
            warn('libroadrunner was not found, please install libroadrunner')
        return res_ar
