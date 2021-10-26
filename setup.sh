echo "starting setup..."
echo " "

echo "making 'ODBM' conda virtual environment..."
conda create -n ODBM python=3.6
conda activate ODBM
pip install biocrnpyler
pip install libroadrunner
echo " "

echo "running tests"
#coverage run -m unittest tests/test.py
echo " "

echo " all done!"