Rem Windows batch script to set up the python environment in the PWD
call python -m venv %~dp0\python_environment  
call python_environment\Scripts\activate.bat  
call python -m pip install --upgrade pip
call pip install numpy opencv-python pillow imutils

