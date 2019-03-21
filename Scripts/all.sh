#!/bin/bash

####################################################################
#               Author : Benjamin Vignau                           #
#               contact : benjamin.vignau1@uqac.ca                 #
#                                                                  #
#       Bash script to create propagation graph for each pool      #
####################################################################


liste=`ls | grep .csv`
for classF in $liste
do
    python features_propagation.py $classF
done
