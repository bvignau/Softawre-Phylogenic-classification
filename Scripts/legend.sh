#!/bin/bash
path="$1key1.txt"
echo "path = $path"
key1=$(cat $path)
path="$1key2.txt"
key2=`cat $path`
path="$1edges.txt"
edges=`cat $path`
path="Propagationv2_$1.dot"
img="Propagationv2_$1.jpg"
echo "key1 = $key1"
nbligne=`wc -l $path | cut -d" " -f1`
let nbligne--
npath="Legendv2_$path"
head -$nbligne $path > $npath 
echo "{
    graph [rank = max]
    node [shape=plaintext
    height = 25,
	  fontsize=60,
	  width=20]
    label = \"Legend\";
    key [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">
        $key1
      </table>>]
    key2 [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">
        $key2
      </table>>]
    $edges
  }
}" >> $npath

dot -Tjpg $npath -o $img