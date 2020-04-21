# Software Phylogenic graphs generation

This project gather all scripts and data used to create our Phylogenic graph and our feature propagation multigraph. 

## Getting Started

These instructions will get you a copy of our data and algorithms to generate graphs. Feel free to use and modify them for research and educational purpose only.

### Prerequisites

Our scripts use Bash, Graphviz and Python 3.6. Pygraphiz, Cairo, Turtle and dot are mandatory to run our project. Use the following commands to install all the prerequisites.

```
sudo apt-get install graphviz
```

```
pip install cairosvg pygraphviz
```

### Installing

To run our scripts, you need to create a csv file with a row for each feature and a column for each software. Put a 1 when software use a feature, 0 if not. The CSV seperator need to be ';'. The first column is the name of each features, the first row is the name of each software with its date, separate with a '-'. For example, see features.csv in the data folder.
To run our scripts, just put all of them in a folder with csv file and use the following command. Please don't use space in the name of the malware or features.

For features propagation :
```
python features_propagation.py file.csv
```

To process multiples files like us, put all csv files in the Scripts folder. Then execute the `all.sh` script. It will create all the composant to create a graph. Use the `order.sh` script to split the results. It will put the 'goal items' in the RES1 folder, the 'infection items' in RES2, 'organisation items' in RES3 and 'efficiency items' in RES4.

To improve the readability of our graphs, we use the SVG items in a yed editor (https://www.yworks.com/yed-live/) and recreate the graph thaks to the dot file. If you want, png files are also availables.

Our results : 

All our graphs with differents layout are in the figure/graph directory. The figures/palette contains the fours palettes to recreate our graph in YED. The graphml of our files are in the graphml folder. 

Goal graph, YED Version :

![Goal jpg YED](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/figures/Goal_final.png)

Goal graph, dot Version :

![Goal jpg dot](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/figures/goal.png)

Infection graph, orhtogonal_router configuration, YED :

![infection jpg router_ortho](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/figures/infection_v2_ortho_router.png)

Infection graph, baloon configuration, YED :

![infection jpg baloon](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/figures/infection_v2_ballon.png)

Infection graph, dot :

![infection jpg dot](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/figures/infection.png)







## Authors

* **Benjamin Vignau** 



## License

This project is available for all research and educational purpose only.


