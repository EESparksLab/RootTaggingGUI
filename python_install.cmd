##Windows batch script to set up the python environment in the PWD
python3 -m venv %~dp0\python_environment  #Creates a new virtual environmnet in PWD
source %~dp0\python_environment\Scripts\activate.bat  #swithces to our new virtual environment
python3 -m pip install --upgrade pip
pip install numpy opencv-python pillow imutils

