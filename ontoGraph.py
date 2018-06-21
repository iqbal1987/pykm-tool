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
from StatementParser import SParser
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

        self.SP=SParser()
        self.currfilepath='test-output' # couldnot append a \ emits error. for now add insitu.
        self.defaultfilname='New_og_file'
        self.defaultfileext='.og'
        self.lines=[]
            
    def __str__(self):
        return str(self.baseNode)+": OntoGraph Object"

    def __len__(self):
        return self.currLength

    def addNode(self,Nname="Node",p=None,s=None):
        #print(type(Nname))
        if type(Nname)==Node:
            if not(str(Nname) in [str(i) for i in self.nList]):
                self.nList.append(Nname)
                self.currLength=len(self.nList)
            else:
                error('Node '+str(Nname)+' already exists.')
        elif type(Nname)==str:
            #print([str(i) for i in self.nList])
            if not(Nname in [str(i) for i in self.nList]):
                tmp=Node(name=Nname,pred=p,succ=s)
                self.nList.append(tmp)
                self.currLength=len(self.nList)
            else:
                error('Node '+str(Nname)+' already exists.')
        else:
            error('Node cannot be added datatype mismatch.')

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
            pass
        elif action=='insertObject':
            pass
        else:
            error('Invalid assign command')
    
    def parseStmt(self):
        self.lines=self.fetchStatement('testInput')
        self.lineTokens=self.SP.genToken(self.lines[0],True)
        isThingSet=False
        for i in self.lineTokens:
            Nlist=[str(ni) for ni in self.nList]
            T=self.lineTokens[i]
            gramType=[t.typ for t in T]
            gramLevel=[]
            for t in T:
                if not t.pos==[]:
                    gramLevel.append(t.level+str(t.pos[0]))
                else:
                    gramLevel.append(t.level)
                
            gramVal=[t.value for t in T]
            gramPos=[t.pos for t in T]
            #print(gramType)
            print(gramLevel)
            #print(gramPos)
            #print(gramVal)
            print('\n')
            if not(T[0].level=='COMMENT'):
                if not isThingSet:
                    if T[2].value=='Thing':
                        self.addNode(T[0].value,p='Thing')
                    else:
                        self.addNode(T[0].value,p='Thing')
                        print('First concept/object in a domain should be a sub-class of Thing.\nConcept '+T[0].value+' is defined a super-class ''Thing'' automatically.')
                    isThingSet=True
                    #print([str(ii) for ii in self.nList])
                else:
                    # first element (subject) has to be level:0, check already done inside statment parser.
                    # start with second element (verb of the predicate). predicate = verb+noun
                    if T[1].level=='k1':
                        #check if the subject exists
                        if (T[0].typ=='0' and T[0].value in Nlist):
                            # look ahead to check if k2 verbs exists
                            pass
                            
                        
    def fetchStatement(self,filename=None,fileext='.og'):
        #if not filename==None:
        fileHandle=open(self.currfilepath+'\\'+filename+fileext,'r')
        lines=fileHandle.readlines()
        fileHandle.close()
        return lines
        
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
           
if __name__=="__main__0":
    g=OntoGraph(name='FESS')
    print(g.currLength)
    g.addNode(Node("Node1","y"))
    print(g.listNodes())
    g.nList[1].addProp('X')
    g.addNode(Node("Node2"))
    print(g.listNodes()) 
    g.addNode("Node3",'a','b')
    print(g.listNodes())
    
if __name__=="__main__":
    g=OntoGraph(name='FESS')
    g.parseStmt()
    #print(g.lines)
