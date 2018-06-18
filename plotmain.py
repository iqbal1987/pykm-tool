# -*- coding: utf-8 -*-
"""
Created on Wed May 23 21:09:56 2018

@author: Mohamme Iqbal

This is Plot main
Extra comment
third comment
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bezierArrow import *
from visualization import VisualizeOnto
from DraggableArtist import DraggableRectangle, DraggableText

v=VisualizeOnto()
v.createDot()
v.makeLayout()
v.readLayout()
g,n,e=v.getLayout()

# Initialize Figure

fig = plt.figure()
ax=fig.add_subplot(111)
rH=[None]*len(n)
txtH=[None]*len(n)
tH=[None]*len(n)

# Plot Nodes
for i in range(len(n)):
    xcorner=n[i+1]['xy'][0]-n[i+1]['w']*0.5
    ycorner=n[i+1]['xy'][1]-n[i+1]['h']*0.5
    rH[i]=ax.add_patch(Rectangle((xcorner,ycorner),n[i+1]['w'],n[i+1]['h']))
    #txtH[i]=ax.text(xcorner,ycorner,'Node 2',size=12,ha='center',va='center',bbox=dict(boxstyle='square'))
    tH[i]=ax.text(n[i+1]['xy'][0],n[i+1]['xy'][1],'Node '+str(i+1),size=12,ha='center',va='center')


# Plot Arrows
aH=[]
for i in range(len(e)):
    bp=e[i]['pts']
    aH.append(bezierArrow(ax,np.array([[i[0] for i in bp],[i[1] for i in bp]]),arrowDir='end'))

# find Node - Edge relation or later find it from adjacency Matrix
nodes_tails=[]
nodes_heads=[]
for i in range(len(e)):
    #print(i)
    nodes_tails.append([e[i]['tail'],i]) # (nodeID,edgeID[tail])
    nodes_heads.append([e[i]['head'],i])# (nodeID,edgeID[head])
n_heads={}
n_tails={}
for i in range(len(n)):
    n_heads.update({i+1:[ind for n,ind in nodes_heads if n==i+1]}) # since nodeIDs start from 1 (graphviz)
    n_tails.update({i+1:[ind for n,ind in nodes_tails if n==i+1]})
 
# Create draggable rectable from node objects
drs=[]
rcnt=1
for rect in rH:#txtH
    dr=DraggableRectangle(rect,rcnt,n_heads,n_tails,aH,tH)
    #dr=DraggableText(rect,rcnt,n_heads,n_tails,aH)
    dr.connect()
    drs.append(dr)
    rcnt+=1

# plot text nad make it daggable
txt2=ax.text(0.0,0.0,'Node 2',size=12,ha='center',va='center',bbox=dict(boxstyle='square'))
ar=DraggableText(txt2)
ar.connect()


# getCurrentPositions of all objects and store them (make a separate function of the class)
# rH,aH,tH
# for not losing the position data of the nodes (deliberatly changed by the user
# node id, edge id preserve as far as possible. before reading the new dot file.


# Plot the axis + setup bleed gap in the edges
bleedw=g['scale']*g['w']*0.1
bleedh=g['scale']*g['h']*0.1
ax.set_xlim(0-bleedw,g['scale']*g['w']+bleedw)
ax.set_ylim(0-bleedh,g['scale']*g['h']+bleedh)
fig.tight_layout()
plt.show()


