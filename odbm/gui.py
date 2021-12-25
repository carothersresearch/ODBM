from tkinter import *
from os.path import exists
# issue with import statement - odbm is not a package?
from odbm import *
# I think maybe moving things into classes would make more sense here

# 2nd Window
def modelWindow():
    # close old window (not defined here?)
    frame.destroy()
    # Open new window
    root = Tk()
    frame = Frame(root)
    frame.pack()

    cancel_button = Button(frame, text="Cancel", fg="blue") # need a command to restart/reinitialize main window
    simulate_button = Button(frame, text = 'Simulate Model', fg = 'blue') # need a command to open simulate window
    edit_button = Button(frame, text = 'Edit Model', fg = 'blue') # need a command to open edit window


# Checks if model path given by user exists and builds model.
def loadModel(entry):
    global myModel #create global variable so it is accessible in main
    model_path = entry.get()
    if exists(model_path) and model_path.endswith('.xls','.xlsx'):
        model_species = pd.read_excel(model_path, sheet_name = 'Species & Base Mechanisms', engine = 'openpyxl').dropna('index','all')
        model_rxns = pd.read_excel(model_path, sheet_name = 'Reaction', engine = 'openpyxl').dropna('index','all')
        myModel = ModelBuilder(model_species, model_rxns)
        modelWindow(myModel)
    else:
        if exists(model_path):
            raise('Please pass in an excel compatible workbook with sheets named "Species & Base Mechanisms" and "Reaction"')
        else:
            raise('Error: No file exists with given name.')



# Main Window
root = Tk()
frame = Frame(root)
frame.pack()

welcome = Label(frame, text = "Welcome to ODBM \n Please insert file path for model to load:")
welcome.config(font = ('Arial', 12))
entry = Entry(frame)
loadbutton = Button(frame, text="Load Model", fg="blue", command = loadModel(entry))

welcome.pack()
loadbutton.pack(side = BOTTOM)
entry.pack()
root.mainloop()

