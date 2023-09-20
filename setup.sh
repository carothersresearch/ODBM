echo "starting setup..."
echo " "

echo "making 'ODBM' conda virtual environment..."
conda create -n ODBM python=3.6
activate ODBM
pip install tellurium==2.1.5
pip install xlrd==1.2.0
pip install openpyxl==3.0.0
pip install notebook==6.3.0

echo " "

echo "running tests"
#coverage run -m unittest tests/test.py
echo " "

echo " all done!"