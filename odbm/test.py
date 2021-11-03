from biocrnpyler import *
from odbm import DCRN

A = Species("A", material_type = "m1", attributes = ["attribute"])
B = Species("B", material_type = "m1")
C = Species("B", material_type = "m2")
D = Species("D")

print("Species can be printed to show their string representation:", A, B, C, D)

#Reaction Rates
k1 = 3.
k2 = 1.4
k2rev = 0.15

#Reaciton Objects
R1 = Reaction.from_massaction([A], [B, B], k_forward = k1)
R2 = Reaction.from_massaction([B], [C, D], k_forward = k2)

print("\nReactions can be printed as well:\n", R1,"\n", R2)

#Make a CRN
CRN = DCRN(species = [A, B, C, D], reactions = [R1, R2])

#CRNs can be printed in two different ways
print("\nDirectly printing a CRN shows the string representation of the species used in BioCRNpyler:")
#print(CRN)

print("\nCRN.pretty_print(...) is a function that prints a more customizable version of the CRN, but doesn't show the proper string representation of species.")
#print(CRN.pretty_print(show_materials = True, show_rates = True, show_attributes = True))

try:
    import roadrunner
    x0 = {str(A):120}
    xt = {str(A):lambda t: 10*t}
    timepoints = range(0,10)
    result = CRN.simulate_with_roadrunner(timepoints, initial_condition_dict = x0, dynamic_condition_dict = xt)
    import pylab
    pylab.plot (result[:,0],result[:,1:])
    pylab.xlabel('time')
    pylab.ylabel('concentration')
    pylab.show()
except ModuleNotFoundError:
    warnings.warn('libroadrunner was not found, please install libroadrunner')