::  # # # # # # # # # # # # # # # # # # # # # # # # #
::  # Updated 2023/06/20: Make simplier by rathaROG #
::  # # # # # # # # # # # # # # # # # # # # # # # # #

@echo off
setlocal
cd /d %~dp0
set "PYTHONWARNINGS=ignore"
python -m pip install --upgrade pip
pip install wheel
pip install build
python -m build --wheel --skip-dependency-check --no-isolation
pause
