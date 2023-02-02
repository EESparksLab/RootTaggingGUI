#!/bin/bash
#This is a wrapper that launches program
#its not great... but it works for now (5/31/22)
source ./python_environment/bin/activate   # Uses custom python envionment in PWD
#credit to William Cantera (wcantera@udel.edu), this is his code from the original build
PYWRAP=$(cat <<EOF
import tagging
import tagging.tagger_controller
tagging.tagger_controller.start()
EOF
)
#BASH Variable to pass to python

python3 -c "$PYWRAP"  #Executes the python wrapper
