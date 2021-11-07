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


## Example: Defining Models from Excel

![excel_species](/static/excel_species_ex.png)
Every species must have a **Label, Type, and Starting Conc**. 
  * Label can contain any characters and will be processed by ODBM to be compatible with Tellurium. 
  * Accepted Types include DNA, RNA, Enzyme, Cofactor


*TO-DO: Users can create own type?
 
 
![excel_rxn](/static/excel_rxn_ex.png)
Define chemical reactions with a **Label, Mechanism, Substrate, Product, and Parameters**. Enzyme and Cofactor are optional.
  * Accepted Mechanisms are Michaelis-Menten ("MM"), Mass Action ("MA"), Ordered Bi-Bi substrate ("OBB"), and Product-Inhibition ("PI").
    * Mechanisms are defined as classes and users can create custom mechanisms by defining a new class in *mechanisms.py*
    * Users do NOT need to define every step of the process if their input is DNA. e.g., do not need to write a reaction for
      DNA + RNAP --> RNAP + RNA
      RNA + Ribosome --> AA + Ribosome
    * ODBM will handle these cases automatically.

 *TO-DO: Can PI be mono or bi-substrate? Do these require different mechanisms?
 *TO-DO: Need to figure out how we handle transcription/translation. Are RNAP and Ribosome fixed species?

![model_txt](/static/model_txt_ex.png)
* ODBM will output an easy-to-read string that is Tellurium compatible and SBML compliant. From here, users can simulate their model using roadrunner.

*TO-DO: 
* add plots of simulation
