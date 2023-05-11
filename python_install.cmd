Rem Windows batch script to set up the python environment in the PWD
Rem Create a virtual environment for Python in the current working directory
call python -m venv %~dp0\python_environment

Rem Activate the virtual environment
call python_environment\Scripts\activate.bat

Rem Upgrade pip to the latest version
call python -m pip install --upgrade pip

Rem Install required Python packages
call pip install numpy opencv-python pillow imutils
