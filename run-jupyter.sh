#!/bin/bash

source venv/bin/activate
python scripts/setup_database.py
cd notebooks
jupyter notebook
