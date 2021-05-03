rm -r docs/
sphinx-apidoc -o docs/ ../chai_py --separate
make html
