echo "starting setup..."
echo " "

echo "making 'ODBM' conda virtual environment..."
conda create -n ODBM python=3.6
activate ODBM
pip install tellurium
pip install pandas
pip install xlrd
pip install openpyxl
pip install overrides
pip install notebook

echo " "

echo "running tests"
#coverage run -m unittest tests/test.py
echo " "

echo " all done!"