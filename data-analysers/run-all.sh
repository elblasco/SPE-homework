#!/usr/bin/env bash

if ! [ -d .venv/ ]; then
   python -m venv .venv || exit;
   source .venv/bin/activate || exit;
   pip install -r requirements.txt || exit;
else
    source .venv/bin/activate || exit;
fi



for file in *.py; do
    echo -e "\nRUNNING $file";
    python $file || exit;
done

echo -e "\nThe charts are under ./img/"