###########################################################################
#                          Author : Benjamin Vignau                       #
#                   contact : benjamin.vignau1@uqac.ca                    #
#                                                                         #
#    python 3.6 script to calcul and create propagation features graph    #
#        usage : python3 features_propagation.py sample.csv               #
###########################################################################



import os
import sys
import argparse
import turtle
import canvasvg
import tempfile
import cairo
from pygraphviz import *
import turtle


COLOR=["navy", "burlywood", "cyan","red",
    "forestgreen","magenta","gold", "springgreen", 
    "purple","orangered","sienna","grey","pink",
    "yellow", "brown","crimson","orange",
    "chocolate", "aquamarine","turquoise"] # color dict, change to add more colors

class Logiciel:
    
    def __init__(self, nom, annee,num):
        self.nom = nom                # software name
        self.date = annee
        self.features = dict()       # features list (1 if posses 0 if not)
        self.distance = dict()
        self.commun = dict()
        self.Tfeature = 0
        self.num = num
        self.Ifeatures=0

class Feature:
    def __init__(self, nom, annee, soft, num):
        self.nom = nom
        self.date = annee
        self.soft = list()
        self.softwares = dict()
        self.TSoft = 0
        self.num = num
        self.dashed = False

# function to parse a CSV File (; as separator) containing in 1st row ;SoftwareName-Year.Month;

def ParseCSV(sample,CSV,features):
    compteur=0
    name_list=[]
    num = 0
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
                    features[fctn]=Feature(fctn,0," ",i)
                    i +=1

def AfficheLogiciel(sample,features):
    for logiciel in sample.values():
        print(logiciel.nom)
        for f, v in logiciel.features.items():
            if v == '1' :
                print(f)
        print("*******************************")


def AfficheFeatures(features):
    for f,v in features.items() :
        print("feature = "+f)
        print("date = "+str(v.date))
        print("softwares = "+str(v.softwares))
        print("*******************************")

# function to find which malware create which features and to find which malware use which feature
def CalculFeatures(sample,features):
    for soft in sample.values() :
        for f,v in soft.features.items():
            if v == '1':
                if features[f].date == 0:
                    features[f].date = soft.date
                    features[f].soft.append(soft.nom)
                    features[f].TSoft+=1
                    soft.Ifeatures+=1
                elif abs(float(features[f].date) - float(soft.date)) < 0.06:
                    features[f].TSoft+=1
                    features[f].softwares[soft.nom]=soft.date
                    features[f].soft.append(soft.nom)
                else :
                    features[f].TSoft+=1
                    features[f].softwares[soft.nom]=soft.date

# Function to create the propagation feature graphe
def PropagationFeatures(sample,features, titre, circles):
    name="Propagation_"+titre
    G=AGraph(strict=False,directed=True, size="100,100", overlap="scalexy",ranksep="1.2",nodesep="1.5",fontsize="80")
    edges=[]
    for nom in sample.keys() :
        lab=nom
        colorN=nom+"_"+titre
        size = sample[nom].Tfeature + 7
        if size > 7 :
            G.add_node(lab,color=colorN,shape='circle', fixedsize=True, width=str(size), height = str(size),fontsize="0", penwidth=0)
            circles[nom]={"size":size}
            d = sample[nom].date
            if  float(d) == 2008.0: # just to have a better position, change and adpat to sample
                G.add_subgraph(nom,rank='min')
            elif float(d) == 2018.0:
                G.add_subgraph(nom,rank='max')
            else :
                G.add_subgraph(nom,rank='same')
    i=0
    dashed = False  # change node and arcs style if not enougth colors
    edgesC={}
    father=[]
    for f in features.values():
        if len(f.soft) > 0 :
            father = f.soft[:]
            if dashed == False :
                for fa in father :
                    circles[fa][COLOR[i]]=False # create circle around the software which create the feature
            else :
                f.dashed = True
                for fa in father :
                    circles[fa][COLOR[i]]=True # create circle around the software which create the feature
            father=f.soft[0]
            for soft in f.softwares.keys(): # propagation of each features in each softwares
                print(str(father))
                fatherN = father
                nodeN = soft
                lab=f.nom
                if dashed == False :
                    if abs(float(sample[fatherN].date) - float(sample[nodeN].date)) > 0.06:
                        G.add_edge(fatherN,nodeN,color=COLOR[i], style="bold", penwidth=5.5,arrowtail="none", labeldistance=20, labelfloat=True)
                else :
                    f.dashed = True
                    if abs(float(sample[fatherN].date) - float(sample[nodeN].date)) > 0.06:
                        G.add_edge(fatherN,nodeN,color=COLOR[i], style="dashed", penwidth=5.5,arrowtail="none", labeldistance=20, labelfloat=True)
                #father=soft
            edgesC[f]=COLOR[i]
            if i < 18:
                i+=1
            else :
                i = 0
                dashed = True
    print("*******************")
    filename=titre+".txt"
    fichier=open(filename,"w")
    for nom,node in circles.items():
        colors={}
        size =0
        for c,d in node.items():
            if c == "size":
                size = d
            else :
                colors[c]=d
        name=nom+"_"+titre
        
        # faire la liste des 
        create_shape(name,size,colors,sample[nom].date)
        name=name+"\n"
        fichier.write(name)
    fichier.close()
    name="Propagationv2_"+titre+".dot"
    G.write(name)
    genLegend(edgesC,titre)
    finalname="Legendv2_"+name
    cmd="./ajoutImage.sh "+filename+" "+finalname
    os.system(cmd)
    # supprimer les espaces
    # appel script bash


# funciton to generate the legend
def genLegend(edgesC,titre):
    key1=titre+"key1.txt"
    key2=titre+"key2.txt"
    edges=titre+"edges.txt"
    Key1fichier=open(key1,"w")
    Key2fichier=open(key2,"w")
    edgesfichier=open(edges,"w")
    i = 0
    for feature, color in edgesC.items():
        tk1 = "<tr><td align=\"right\" port=\"i"+str(i)+"\">"+str(feature.nom)+"</td></tr>"
        tk2 = "<tr><td port=\"i"+str(i)+"\">&nbsp;</td></tr>"
        if feature.dashed == False :
            te = "key:i"+str(i)+":e -> key2:i"+str(i)+":w [color="+str(color)+", style=bold, penwidth=10]"
        else :
            te = "key:i"+str(i)+":e -> key2:i"+str(i)+":w [color="+str(color)+", style=dashed, penwidth=10]"
        Key1fichier.write(tk1)
        Key1fichier.write('\n')
        Key2fichier.write(tk2)
        Key2fichier.write('\n')
        edgesfichier.write(te)
        edgesfichier.write('\n')
        i+=1
    Key1fichier.close()
    Key2fichier.close()
    edgesfichier.close()
    os.system("./legend.sh "+titre)



def CalculLimite(sample):
    for s in sample.values():
        tf = 0
        for f in s.features.values() :
            tf = tf+int(f)
        s.Tfeature=tf
        print(s.nom + "= "+str(s.Tfeature))



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

def CalculCommun(sample):
    for s in sample.values() :
        for s2 in sample.values() :
            common =0 
            if s != s2 :
                for f,v in s.features.items() :
                    if v == s2.features[f] and int(v) != 0:
                        common +=1
                s.commun[s2.nom]=common

def AfficheDistance(sample):
    for s in sample.values():
        print(s.nom)
        print(s.distance)
        print("************************")

def AfficheCommun(sample):
    for s in sample.values():
        print(s.nom)
        print(s.commun)
        print("************************")

#function to generate dashed circle with turtle
def dashed_circle(r):
    for j in range(0,380,20):
        turtle.pendown()
        turtle.circle(r,10)
        turtle.penup()
        turtle.circle(r,10)

#function to create shape of each node, in function of features it create
def create_shape(nom,size,color,date):
    turtle.screensize(2000,2000)
    turtle.speed("fastest")
    turtle.penup()
    radius = 250+(size*30)
    malwarename=nom.split('_')
    namem=malwarename[0]
    turtle.right(90)    # Face South
    turtle.forward(radius/4-75)   # Move one radius
    turtle.right(270)
    turtle.write(namem, move=False, align="center", font=("Arial", int(80+size), "bold"))
    turtle.home()
    turtle.right(90)    # Face South
    turtle.forward(radius/3+75)   # Move one radius
    turtle.right(270)
    turtle.write(date, move=False, align="center", font=("Arial", int(80), "bold"))
    turtle.home()
    turtle.pensize(15)
    turtle.right(90)    # Face South
    turtle.forward(radius)   # Move one radius
    turtle.right(270)
    turtle.pendown() 
    turtle.circle(radius)
    turtle.penup()      # Pen up while we go home
    turtle.home()
    for c,d in color.items():
        radius+=75
        turtle.right(90)    # Face South
        turtle.forward(radius)   # Move one radius
        turtle.right(270)   # Back to start heading
        turtle.pencolor(c)
        turtle.pendown()    # Put the pen back down
        if d == True :
            dashed_circle(radius)
        else:
            turtle.circle(radius)
        turtle.penup()      # Pen up while we go home
        turtle.home()
    turtle.hideturtle()
    svg = nom+".svg"
    png = nom+".png"
    print("svg ="+svg)
    print("png ="+png)
    ts = turtle.getscreen().getcanvas()
    canvasvg.saveall(svg, ts)
    cmd="cairosvg "+svg+" -o "+png
    os.system(cmd)
    turtle.reset()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fichier')
    args = parser.parse_args()
    Ifichier=open(args.fichier,"r")
    titre=args.fichier.split(".")[0]
    print("##############################################")
    print("##########     "+titre+"     ##########")
    print("##############################################")
    inputCSV=Ifichier.read()
    Ifichier.close()
    sample={}
    features = {}
    circles = {}
    ParseCSV(sample,inputCSV,features)
    CalculDistance(sample)
    CalculLimite(sample)
    CalculFeatures(sample,features)
    AfficheLogiciel(sample,features)
    AfficheFeatures(features)
    PropagationFeatures(sample,features,titre,circles)


    

if __name__ == '__main__':
    main()
