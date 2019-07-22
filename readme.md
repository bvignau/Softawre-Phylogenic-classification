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
To run our scripts, just put all of them in a folder with csv file and use the following command.

For the phylogenic graph :

```
python distance_fct.py file.csv
```

Our results : 

features families : 

![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Family-features-graph.svg)

![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Families-circular.svg)

Phylogenic graphe : 

![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Max_Common_V4_15-dot.jpg)

For features propagation :
```
python features_propagation.py file.csv
```
Our results : 
![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Legendv2_Propagationv2_attack.jpg)
![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Legendv2_Propagationv2_features.jpg)

To generate features propagation graphes for multiples sample, put all csv files in the same folder and run
```
./all.sh
```



## Authors

* **Benjamin Vignau** 



## License

This project is available for all research and educational purpose only.


