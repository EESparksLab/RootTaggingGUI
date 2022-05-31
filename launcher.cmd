## I hate windows
##Switches to custom python environment and runs the program

source %~dp0\python_environment\Scripts\activate.bat  #swithces to our new virtual environment
set PYWRAP = import tagging%nl%import tagging.tagger_controller%nl%tagging.tagger_controller()
python3 -c %PYWRAP%

