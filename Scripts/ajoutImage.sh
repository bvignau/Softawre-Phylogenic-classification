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
    r="image=\"$soft.svg\""
    cmd="s/$f/$r/g"
    sed -i -r $cmd $2
done
nom=`echo $2 | cut -f1 -d"."`
out="$nom.pdf"
echo "in = $2"
echo "out = $out"
dot -Tpdf $2 -o $out -Goverlap=false
cp $out ../
#rm *.svg
#rm *.jpg
#rm *.png
#rm *.txt
#rm *.dot