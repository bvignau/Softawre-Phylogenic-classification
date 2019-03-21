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
![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Max_Common_V4_15-dot.jpg)

For features propagation :
```
python features_propagation.py file.csv
```
Our results : 
![alt text](https://github.com/bvignau/Softawre-Phylogenic-classification/blob/master/Graphes/Legendv2_Propagationv2_attack.jpg)

To generate features propagation graphes for multiples sample, put all csv files in the same folder and run
```
./all.sh
```



## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

