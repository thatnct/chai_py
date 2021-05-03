rm -r docs/source
sphinx-apidoc -o docs/source ../chai_py --separate
make html
