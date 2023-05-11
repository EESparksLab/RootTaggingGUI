@echo off
rem = """
rem Setting custom environment variable

call python_environment\Scripts\activate.bat
rem calls the Python interpreter, tells it to skip the first line of the script, and passes it the full path of the current script as well as any command-line arguments.
call python -x "%~f0" %*
goto endofPython """

# Your python code goes here ..

import tagging
import tagging.tagger_controller
tagging.tagger_controller.start()

rem = """
:endofPython """
