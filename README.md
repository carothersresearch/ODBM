# Optimization of Dynamic Bioconversion Modules (ODBM)

## What is ODBM?
  OBDM is a package that helps users build SBML models with Tellurium by interfacing with an Excel spreadsheet. Users can define their species, reactions, and mechanisms in an intuitive way and automatically construct their SBML model with Tellurium. The creation of large mechanistic models that encompass the entire central dogma (DNA -> RNA -> Protein -> Function) quickly become unweildy as users must define the species and reaction at every step of the process. ODBM simplifies this by baking in the steps of trancsription and translation of a given species of DNA that will eventually become an Enzyme.

  
## Who is ODBM for?
  ODBM is made for the experimentalist with limited Python knowledge. However, with just a little Python experience, users can take full advantage of ODBM to define there own custom reaction mechanisms.

## What can I do with ODBM?
  * Cell-free transcription/translation (TXTL) biocatalysis modeling
  * Mechanistic model for the central dogma
  * Dynamic process control (such as optogenetics) implementation into a model
  * Easily compare different gene isoforms, starting conditions, or time and amount of process control 
