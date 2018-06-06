# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:54:21 2018

@author: Mohamme Iqbal

Node class
properties

methods
"""
import inspect
from callError import error

class Node:
    name=None
    bgcol=None # (0,1,1)
    bcol=None # (0,0,0) black
    pred=None
    succ=None
    x=0
    y=0
    textFormat={'font':'Arial','style':'Normal','size':'10'}
    nodeFormat={'color':(0,1,1),'bColor':(0,0,0),'bStyle':'-'}
    prop={'pro':{},
          'fun':{},
          'att':{}
          }
    dynProp={}
    
    def __init__(self,name,pred=None,succ=None):
        self.name=name
        self.pred=pred
        self.succ=succ
        
    def __str__(self):
        return str(self.name)
    
    def addProp(self,pName,pVal=None,ptype='pro'):
        if not (pName in self.prop[ptype].keys()):
            self.prop[ptype].update({pName:pVal})
        else:
            print(error()+': Property already exists')
        
    def addDynProp(self):
        #store only keys in dynProp
        #update the prop dict with the dynamic properties.
        #a.update({var:val,'newdynkey':val}) will update the key if existing and adds id not existing.
        pass

    def setProp(self,pName,pVal,ptype='pro'):
        if pName in self.prop[ptype].keys():
            self.prop[ptype][pName]=pVal
        else:
            print(error()+': Property dosent not exist')

    def getProp(self,ptype=None,arg=[]): # Overloaded Function # old *args
        if len(arg)==0 and ptype==None: 
            return self.prop
        elif (not(ptype==None) and len(arg)>0):
            r={k:v for (k,v) in self.prop[ptype].items() if k in arg}
            if r=={}:
                return None
            else:
                return r
            
    def getTextFormat(self):
        return self.textFormat
    
    def getNodeFormat(self):
        return self.nodeFormat
    
    def setTextFormat(self,font='Arial',style='Normal',size=10):
        self.textFormat.update({'font':font,'style':style,'size':size})
        print(self.textFormat)
    
    def setNodeFormat(self,color=(0,1,1),bColor=(0,0,0),bStyle='-'):
        self.nodeFormat.update({'color':color,'bColor':bColor,'bStyle':bStyle})
        print(self.nodeFormat)
         
if __name__=="__main__":
    a=Node("node1","prev")
    print(a.name)
    print(a.pred)
    print(a.succ)
    """
    a.setTextFormat(size=20)
    a.setNodeFormat(bColor=(1,1,1))
    """
    a.addProp('energy',10)
    a.addProp('power',20)
    a.addProp('energy',90,ptype='att')
    a.addProp('energy',190,ptype='att')
    a.addProp('speed')
    a.setProp('power',100)
    print(a.getProp())
    print(a.getProp(arg=['speed','energy'],ptype='att'))


