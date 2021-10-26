from biocrnpyler import ChemicalReactionNetwork as CRN
from typing import Dict, List, Tuple, Union
import libsbml
from warnings import warn
import numpy as np

class DCRN(CRN):

    def simulate_with_roadrunner(self, timepoints: List[float], initial_condition_dict: Dict[str,float]=None, dynamic_condition_dict: Dict[str,float]=None, return_roadrunner=False, check_validity=True):
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
                
                flag = 0
                t0 = timepoints[0]
                for t in timepoints[1:]:

                    for key, func in dynamic_condition_dict.items():
                        rr.model[f'[{key}]'] = func(t0)

                    if flag == 0:
                        results = np.array(rr.simulate(t0, t))
                        flag = 1
                    else:
                        results = np.concatenate([results, np.array(rr.simulate(t0, t))])
                    t0 = t

                res_ar = results
        except ModuleNotFoundError:
            warn('libroadrunner was not found, please install libroadrunner')
        return res_ar
