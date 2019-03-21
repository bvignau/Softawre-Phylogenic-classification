#!/bin/bash


####################################################################
#               Author : Benjamin Vignau                           #
#               contact : benjamin.vignau1@uqac.ca                 #
#                                                                  #
#        Bash script to replace color tag by created shape         #
####################################################################

for soft in `cat $1`
do 
    f="color=$soft"
    r="image=\"$soft.png\""
    cmd="s/$f/$r/g"
    sed -i -r $cmd $2
done
nom=`echo $2 | cut -f1 -d"."`
out="$nom.jpg"
dot -Tjpg $2 -o $out -Goverlap=false