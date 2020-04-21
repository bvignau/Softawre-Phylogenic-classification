####################################################################
#               Author : Benjamin Vignau                           #
#               contact : benjamin.vignau1@uqac.ca                 #
#                                                                  #
#       python 3.6 script to calcul and create pylogenic graph     #
#           usage : python3 distance_fct.py sample.csv             #
####################################################################



import os
import sys
import argparse
import turtle
import canvasvg
import tempfile
import cairo
from pygraphviz import *

class Logiciel:
    
    def __init__(self, nom, annee,num):
        self.nom = nom                  # software name
        self.date = annee               # software year
        self.features = dict()          # features list (1 if posses 0 if not)
        self.distance = dict()          # distance dict
        self.commun = dict()            # common dict
        self.Tfeature = 0               # total features
        self.num = num                  # number of the malware in pool


# function to parse a CSV File (; as separator) containing in 1st row ;SoftwareName-Year.Month;
def ParseCSV(sample,CSV,features):
    compteur=0
    name_list=[]
    num = 1
    for ligne in CSV.split("\n"):
        if compteur == 0:
            c2 = 0
            for col in ligne.split(";"):
                if c2 > 0:
                    #print(col)
                    nom,date=col.split("-")
                    sample[nom]=(Logiciel(nom,date,num))
                    name_list.append(nom)
                    num = num +1
                    c2 +=1
                else:
                    c2 +=1
            compteur +=1
        else :
            c2 = 0
            i = 0
            fctn=" " # nom de la fonctionnalité
            for col in ligne.split(";"):
                if c2 == 0:
                    fctn=col
                    c2 +=1
                else :
                    sample[name_list[i]].features[fctn]=col
                    features[fctn]=[]
                    i +=1

# function to show all softwares and all their features
def AfficheLogiciel(sample,features):
    for logiciel in sample.values():
        print(logiciel.nom + " = "+str(logiciel.num))
        for f, v in logiciel.features.items():
            if v == '1' :
                print(f)
                features[f].append(logiciel.num)
        print("*******************************")


# function to generate a Latex Table (4 collumns) with name of the feature and number of each software which possess the feature
def AfficheFeatures(features):
    c=True
    for f,l in features.items():
        names=""
        i=0
        
        for n in l :
            if i == 0:
                names = names + str(n)
                i =1
            else :
                names = names + ", "+str(n)
        if c == True :
            final = f+" & "+names+" &"
            c = False
        else:
            print(final+f+" & "+names+" &")
            print("\hline")
            c = True

# function to compute the distance score of each software in the pool
# See read.me to further informations

def CalculDistance(sample):
    for logiciel in sample.values() :
        for l2 in sample.values() :
            if logiciel != l2 :
                d = 0
                for f,v in logiciel.features.items() :
                    md = int(v) - int(l2.features[f])
                    md = md**2
                    d = d +md
                logiciel.distance[l2.nom]=d


# function to compute the common score of each software in the pool
# See read.me to further informations

def CalculCommun(sample):
    for s in sample.values() :
        for s2 in sample.values() :
            common =0 
            if s != s2 :
                for f,v in s.features.items() :
                    if v == s2.features[f] and int(v) != 0:
                        common +=1
                s.commun[s2.nom]=common


# function to show the distance score of each software in the pool

def AfficheDistance(sample):
    for s in sample.values():
        print(s.nom)
        print(s.distance)
        print("************************")


# function to show the common score of each software in the pool

def AfficheCommun(sample):
    for s in sample.values():
        print(s.nom)
        print(s.commun)
        print("************************")

# function to generate all Arcs of the phylogenic graph
def genAllEdges(sample,n,G):
    for nom, s in sample.items(): # we create arcs in decreasing order
        cs = s.commun.copy()
        for i in range(n):
            m = max(cs, key=cs.get)
            del cs[m]
            if s.commun[m] > 0 and not G.has_edge(m,nom) and abs(float(s.date) - float(sample[m].date)) > 0.06: # If the 2 software have at least 1 common feature and release date of the former preceeds that of the latter by at least six months.
                G.add_edge(nom, m, color="black", label=str(int(s.commun[m])), style="bold",  penwidth=15,arrowtail="none", labeldistance=25, labelfloat=False,fontsize=80)

# function to generate all Nodes of the phylogenic graph
def genAllNodes(sample,n,G):
    for nom in sample.keys():
        G.add_node(nom,color='red',shape='circle', fixedsize=True, width=str(sample[nom].Tfeature/2), height = str(sample[nom].Tfeature/2),fontsize=str(sample[nom].Tfeature*4 + 2), bold=True, penwidth="5.0")
        d = sample[nom].date
        if float(d) == 2008.0:
            G.add_subgraph(nom, rank='min')
        elif float(d) == 2018.0:
            G.add_subgraph(nom, rank='max')
        else:
            G.add_subgraph(nom, rank='same')


# function to generate the png
def genpng(G,name,layout):
    print("*******************")
    G.write(name+'-'+layout+'.dot')
    G.layout(layout)
    G.draw(name+'-'+layout+'.pdf')

# function to generate the phylogenic graph
def GrapheCommun4(sample,n):
    G=AGraph(strict=False,directed=True,label="Max commun", size="100,100", overlap="scalexy", ranksep="1.5",nodesep="2.5")
    genAllNodes(sample,n,G)
    genAllEdges(sample,n,G)
    for node in sample.keys():  # node
        for n1 in G.successors(node):      # Son
            for n2 in G.successors(n1):    # GSon
                if n1 != n2 and n2 != node: # check no cycle
                    if sample[node].commun[n1] >= sample[node].commun[n2] and G.has_edge(node,n2) and sample[n1].commun[n2] >= sample[node].commun[n2]:   # if Common(N-Son) >= Common(N-GSon) AND Common(Son-GSon >= N-GSon)
                        G.delete_edge(node,n2)  # del N-G Son

    name = "Max_Common_V4_"+str(n)
    layout="dot"
    genpng(G,name,layout)

    
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fichier')
    args = parser.parse_args()
    Ifichier=open(args.fichier,"r")
    inputCSV=Ifichier.read()
    Ifichier.close()
    sample={}
    features = {}
    ParseCSV(sample,inputCSV,features)
    CalculDistance(sample)
    #CalculLimite(sample)
    AfficheLogiciel(sample,features)
    AfficheDistance(sample)
    CalculCommun(sample)
    AfficheCommun(sample)
    AfficheFeatures(features)
    GrapheCommun4(sample,15)


    

if __name__ == '__main__':
    main()
