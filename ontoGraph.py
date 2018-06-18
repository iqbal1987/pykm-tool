# -*- coding: utf-8 -*-
"""
Created on Mon June 4 2018

@author: Mohamme Iqbal

ontoGraph class
properties

methods
"""
from enum import Enum
from node import Node
from StatementParser import SParser as sp
from callError import error

class classID(Enum):
    obj=1
    pro=2
    fun=3
    att=4
    par=5
    parVal=6
    
class OntoGraph:
    name=None
    bgcol=None # (0,1,1)
    bcol=None # (0,0,0) black
    #nodes=None
    currLength=0
    GraphTitle="O-Graph"
    textVal="node"
    textFont="Arial"
    textStyle="Normal"
    textSize=10
    
    baseNode=None
    dynProp={}
            
    def __init__(self,baseNode="Thing",name="Graph Name"):
        self.nList=[]
        # objects or features. Every node has properties{elec:,mech:,chem:}
        # , function, attribute, effect(electrical:{loss},chemical:{interaction,oxidation,pittingcorrosion},mechanical:{friction,}) and so on.
        self.adjMat=[]
        self.nodes={'pro':(),
                    'fun':(),
                    'att':()
                    }
        self.name=name
        self.baseNode=baseNode
        self.nList.append(Node(baseNode))
        self.update()
            
    def __str__(self):
        return str(self.baseNode)+": OntoGraph Object"

    def __len__(self):
        return self.currLength

    def addNode(self,Nname="Node",p=None,s=None):
        print(type(Nname))
        if type(Nname)==Node:
            if not(str(Nname) in [str(i) for i in self.nList]):
                self.nList.append(Nname)
                self.currLength=len(self.nList)
            else:
                error('Node '+str(Nname)+' already exists.')
        elif type(Nname)==str:
            print([str(i) for i in self.nList])
            if not(Nname in [str(i) for i in self.nList]):
                tmp=Node(name=Nname,pred=p,succ=s)
                self.nList.append(tmp)
                self.currLength=len(self.nList)
            else:
                error('Node '+str(Nname)+' already exists.')
        else:
            print('nothing')

    def insertNode(self,node,pre,succ):
        pass

    def removeNode(self, node):
        pass
    
    def setPred(self,n,p):
        if n.name in nList:
            nList[n.name].pred=p
        else:
            error('Node dosent exist')
    
    def setSucc(self,n,s): # extends node
        pass
    
    def getPred(self): # extends node
        pass
    
    def getSucc(self): # extends node
        pass
    
    def getNodesbyId(self,id):
        pass
    
    def getNodesbyName(self,nodes):
        pass   

    def listNodes(self):
        return [str(i) for i in g.nList]

    def assignOnto(self,action,*args):
        if action=='addObject':
            #args[0]:name [1]:prev Node, [2]:next Node [3]:type=classID.xyz
            # addNode(name,p,n,typ)
            # p can be None type for the first node added to the graph.
        elif action=='insertObject':
            pass
        else:
            error('Invalid assign command')
    
    def parseStmt(self):
        pass
    
    def update(self):
        # update something
        # getAdjacency
        # pass to visualize
        # update plot
        pass
        
    def plot(self,canvas):
        pass

    def getAdjacency(self):
        pass
    # return adjacencyMatrix, nList
    # choose for adjacency with prooperties as nodes, fuctions as nodes
    # obj->func->propn obj->prop, relTo->obj, relTo->func
    # obj(function)->prop-relTo->obj2
    # gviz Record with named frames for functions. prps as separate nodes

    def getIncidence(self):
        pass
           
if __name__=="__main__":
    g=OntoGraph(name='FESS')
    print(g.currLength)
    g.addNode(Node("Node1","y"))
    print(g.listNodes())
    g.nList[1].addProp('X')
    g.addNode(Node("Node2"))
    print(g.listNodes()) 
    g.addNode("Node3",'a','b')
    print(g.listNodes())


