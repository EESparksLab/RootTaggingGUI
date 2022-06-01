@echo off
rem = """
rem Do any custom setup like setting environment variables etc if required here ...

call python_environment\Scripts\activate.bat

call python -x "%~f0" %*
goto endofPython """

# Your python code goes here ..

import tagging
import tagging.tagger_controller
tagging.tagger_controller.start()

rem = """
:endofPython """
