#!/usr/bin/env bash

git submodule init
git submodule update
python -m ipykernel install --name seaborn-dev

pushd seaborn
pip install -e .
popd

make -C seaborn/doc notebooks
make -C seaborn/doc html

doc2dash -n Seaborn seaborn/doc/_build/html
python add_samples_tutorial.py
tar --exclude='.DS_Store' -cvzf Seaborn.tgz Seaborn.docset
