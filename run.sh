#!/usr/bin/env bash

git submodule init
git submodule update
python -m ipykernel install --name seaborn-dev

pushd seaborn
pip install -e .
popd

pushd seaborn/doc/tutorial
make
popd

pushd seaborn/doc
make introduction
make html
popd

doc2dash -n Seaborn seaborn/doc/_build/html
python add_samples_tutorial.py
tar --exclude='.DS_Store' -cvzf Seaborn.tgz Seaborn.docset
