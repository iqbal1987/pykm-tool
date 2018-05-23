# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:54:21 2018

@author: Mohamme Iqbal

Node class
properties

methods
"""
class Node:
    name=None
    bgcol=None # (0,1,1)
    bcol=None # (0,0,0) black
    pred=None
    succ=None
    x=0
    y=0
    textFont="Arial"
    textStyle="Normal"
    textSize=10
    
    
    def __init__(self,name,pred=None,succ=None):
        self.name=name
        self.pred=pred
        self.succ=succ
        
if __name__=="__main__":
    a=Node("node1","y")
    print(a.name)
    print(a.pred)
    print(a.succ)    
        


