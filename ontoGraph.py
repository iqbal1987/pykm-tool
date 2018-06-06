# -*- coding: utf-8 -*-
"""
Created on Mon June 4 2018

@author: Mohamme Iqbal

ontoGraph class
properties

methods
"""
from node import Node
from callError import error
class OntoGraph:
    name=None
    bgcol=None # (0,1,1)
    bcol=None # (0,0,0) black
    nodes=None
    currLength=0
    GraphTitle="O-Graph"
    textVal="node"
    textFont="Arial"
    textStyle="Normal"
    textSize=10
    
    baseNode=None
    nList=[]
    prop={'pro':(),
          'fun':(),
          'att':()
          }
    dynProp={}
            
    def __init__(self,baseNode="Thing",name="Graph Name"):
        self.name=name
        self.baseNode=baseNode
        self.nList.append(Node(baseNode))
        self.update()
            
    def __str__(self):
        return str(self.baseNode)+": OntoGraph Object"

    def __len__(self):
        return self.currLength

    def addNode(self,Nname="Node",p=None,s=None):
        tmp=Node(name=Nname,pred=p,succ=s)
        self.nList.append(tmp)
        self.currLength=len(self.nList)

    def insertNode(self):
        pass

    def removeNode(self):
        pass
    
    def setPred(self,n,p):
        if n.name in nList:
            nList[n.name].pred=p
        else:
            error('Node dosent exist')
    
    def setSucc(self,n,s):
        pass
    
    def getPred(self):
        pass
    
    def getSucc(self):
        pass
    
    def getNodesbyId(self):
        pass
    
    def getNodesbyName(self):
        pass   

    def listNodes(self):
        return [str(i) for i in g.nList]

    def assignOnto(self):
        pass
    
    def parseStmt(self):
        pass
    
    def update(self):
        # update something
        pass
        
    def plot(self,canvas):
        pass

    def getAdjacency(self):
        pass # return adjacencyMatrix, nList

    def getIncidence(self):
        pass
           
if __name__=="__main__":
    g=OntoGraph(name='FESS')
    print(g.currLength)
    g.addNode(Node("Node1","y"))
    print(g.listNodes())
    g.nList[1].addProp()
  
        


