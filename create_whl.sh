#!/bin/bash

# # # # # # # # # # # # # # # # # # # # # # # # #
# Updated 2023/06/20: Make simplier by rathaROG #
# # # # # # # # # # # # # # # # # # # # # # # # #

python -m pip install --upgrade pip
pip install wheel
pip install build
python -m build --wheel --skip-dependency-check --no-isolation
