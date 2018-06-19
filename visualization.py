# Use Graphviz layout engine
import re
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from bezierArrow import bezierArrow
import numpy as np

class VisualizeOnto:
    dotFile=None
    def __init__(self):
        self.dotFile=[]
        self.dot=None
        self.g={}
        self.n={}
        self.e={}
        self.nodeShape='box'

    def createExampleDot(self,nList=None,adjMat=None,cmt='Node Graph',fmt='plain',verbose=False):
        self.dot=Digraph(comment=cmt,format=fmt,engine=None)
        self.dot.edge_attr.update(arrowhead='none',tailhead='none',dir='none') # forward back both none
        self.dot.node_attr.update(shape='box')
        self.dot.node('1','Node1')
        self.dot.node('2','Node2\nNode4')
        self.dot.node('3','Node3')
        self.dot.node('4','Node5 is a \nnode\n bla\nbla\nbla') # Fixed: caveat: cannot use keyword node. replace node by something in postprocessing of input text and replace it back.
        self.dot.edges(['12','13'])
        self.dot.edge('3','4')
        if verbose:
            print(self.dot.source)

    def createDot(self,nList=None,adjMat=None,cmt='Node Graph',fmt='plain',verbose=False):
        self.dot=Digraph(comment=cmt,format=fmt,engine=None)
        self.dot.edge_attr.update(arrowhead='none',tailhead='none',dir='none') # forward back both none
        self.dot.node_attr.update(shape=self.nodeShape)
        if nList:
            ncnt=1
            for i in nList:
                self.dot.node(str(ncnt),str(i))
                ncnt+=1
        if nList and (adjMat is not None):
            for i in range(np.size(adjMat,1)):
                for j in np.nonzero(adjMat[i]):
                    if (j.size):
                        for k in j:
                            self.dot.edge(str(i+1),str(k+1))
        if verbose:
            print(self.dot.source)
            
    def getDotSource(self):
        return self.dot.source
    
    #def renderDot(self,dot,pathStr='test-output/',fname='firstGraph.gv',viewBool=False):            
    #   dot.render(pathStr+fname,view=viewBool) 
    
    def makeLayout(self,pathStr='test-output/',fname='firstGraph.gv',viewBool=False):
        # call GV layout with the content of the grapgh
        self.dot.render(pathStr+fname,view=viewBool) 
        #return textfilepath
    
    def readLayout(self,pathStr='test-output/',fname='firstGraph.gv',fmt='plain'):
        fileObj=open(pathStr+fname+'.'+fmt,mode='r')
        g={}
        n={}
        e={}
        ecnt=0;
        linestore=''
        dQuote=False
        interdQuoteabsent=False
        qlinecnt=0
        txtLines=[]
        for line in fileObj:
            #print(line)
            a=re.search('"',line)
            #print(a)
            if (not(a==None) or dQuote):
                # if either a quote is present or a quote was found in the previous line capture line.
                dQuote=True
                if dQuote==True and a==None:
                    # if there was a quote found before and this line dosent have a quote, make a note of quote absence. when the quote appears again stop capturing (see next if statement).
                    interdQuoteabsent=True
                #print(line[:-1] +'---'+line[-1])
                linestore+=line[:-1]+' '
                if (interdQuoteabsent==True and not(a==None)) or (qlinecnt>0 and dQuote==True and  not(a==None)):
                    # if there was quote absent in prev line and this line has a quote. this is the end of line capture.
                    # or if there were some lines inbetween, after detecting a first quote, check the qlinecnt and a quote was detected previously and if a quote is found in this line stop capture. 
                    dQuote=False
                    interdQuoteabsent=False
                    #print(linestore)
                else:
                    qlinecnt+=1
                    continue
            if not(linestore==''):
                txtLines.append(linestore)
                linestore=''
                qlinecnt=0
            else:
                txtLines.append(line)
    
        print(txtLines)
        fileObj.close()
            
        for line in txtLines:
            l=line.split()
            #print(line)
            l0=l[0]
            if l0=='graph':
                    g['scale']=float(l[1])
                    g['w']=float(l[2])
                    g['h']=float(l[3])
            if l0=='node':
                    m=re.search(r'["](.*?)["]',line) # add \\n in linestore+=line+' ' and escape all slashes here to preserve \n latex commands etc.
                    if m:
                        line=re.sub(r'"(.*?)"','Qtext',line)
                        #print(line)
                    k=re.search(r'(?P<name>\w+) (?P<id>.*?) (?P<x>.*?) (?P<y>.*?) (?P<w>.*?) (?P<h>.*?) (?P<txt>\w+) (?P<sty>\w+) (?P<shp>\w+) (?P<col>\w+) (?P<fcol>\w+)',line)
                        #k=re.search(r'(?P<name>\w+) (?P<id>.*?) (?P<x>.*?) (?P<y>.*?) (?P<w>.*?) (?P<h>.*?) ["](?P<txt>\w+)["] (?P<sty>\w+) (?P<shp>\w+) (?P<col>\w+) (?P<fcol>\w+)',line)
                        #k=re.search(r'(?P<name>\w+)\s(?P<iid>.*?)\s(?P<x>.*?)\s(?P<y>.*?)\s(?P<w>.*?)\s(?P<h>.*?)\s("?(?P<txti>.*[^"]?))\s.*?',line)
                        #k=re.search(r'(?P<name>\w+)\s(?P<iid>.*?)\s(?P<x>.*?)\s(?P<y>.*?)\s(?P<w>.*?)\s(?P<h>.*?)(?<="\s)([^"]+)(?="\s).*?',line)
                        #print(k.groupdict())
                    if m:
                        qtxt=m.group(1)
                        #print(qtxt)
                    else:
                        qtxt=l[6]
                        #print(k.groupdict()['txt'])
                    #n.update({int(l[1]):{'xy':[float(l[2]),float(l[3])],'w':float(l[4]),'h':float(l[5]),'txt':qtxt, 'style':l[7], 'shape':l[8],'color':l[9],'fillcolor':l[10]}})
                    n.update({int(k.groupdict()['id']):{'xy':[float(k.groupdict()['x']),float(k.groupdict()['y'])]
                            ,'w':float(k.groupdict()['w']),'h':float(k.groupdict()['h']),'txt':qtxt, 'style':k.groupdict()['sty']
                            , 'shape':k.groupdict()['shp'],'color':k.groupdict()['col'],'fillcolor':k.groupdict()['fcol']}})
            if l0=='edge':
                    #print(l)
                    e_nn=[]
                    e_n=int(l[3])
                    delta=range(1,2*e_n)
                    dell=[i*2 for i in range(2,e_n+2)]
                    for i in range(e_n):
                        #print([i,dell[i],dell[i]+1])
                        e_nn.append([float(l[dell[i]]),float(l[dell[i]+1])])
                        
                    e.update({ecnt:{'tail':int(l[1]),'head':int(l[2]),'n':int(l[3]),'pts':e_nn,'labelxy':None,'style':l[4+e_n*2],'color':l[4+(e_n*2)+1]}})
                    ecnt+=1
        #print(g)
        print(n)
        #print(e)
        self.g=g
        self.n=n
        self.e=e
        
    def getLayout(self):
        return self.g,self.n,self.e
        
    def plotLayout(self): # static plot
        g=self.g
        n=self.n
        e=self.e
        fig, ax=plt.subplots()
        nodeHandle=[]
        #nodeHandle[0]=None
        #print(len(n))
        delX=min([n[i]['xy'][0] for i in n])
        delY=min([n[i]['xy'][1] for i in n])
        for i in range(len(n)):
            xcorner=n[i+1]['xy'][0]-n[i+1]['w']*0.5
            ycorner=n[i+1]['xy'][1]-n[i+1]['h']*0.5
            nH=plt.Rectangle((xcorner,ycorner),n[i+1]['w'],n[i+1]['h'],alpha=0.35)
            nt=plt.text(n[i+1]['xy'][0],n[i+1]['xy'][1],n[i+1]['txt'],color='black')
            #print(i)
            ax.add_patch(nH)
            nodeHandle.append(nH)
        #print(str(nodeHandle[0]))
        bleedw=g['scale']*g['w']*0.1
        bleedh=g['scale']*g['h']*0.1
        ax.set_xlim(0-bleedw,g['scale']*g['w']+bleedw)
        ax.set_ylim(0-bleedh,g['scale']*g['h']+bleedh)

        for i in range(len(e)):
            bp=e[i]['pts']
            #print(np.array([[i[0] for i in bp],[i[1] for i in bp]]))
            aH=bezierArrow(ax,np.array([[i[0] for i in bp],[i[1] for i in bp]]),arrowDir='end')
       
        fig.tight_layout()
        plt.show()
        

if __name__=="__main__":
    v=VisualizeOnto()
    v.createExampleDot()
    v.makeLayout()
    v.readLayout()

    nList=['1','2','3','4','5']
    adj=np.zeros((5,5))
    adj[0,3]=1
    adj[0,2]=1
    adj[2,4]=1
    adj[1,4]=1
    v.createDot(nList,adj,verbose=True)
    
    v.makeLayout()
    v.readLayout()
    v.plotLayout()

    
    #for i in v.n:
    #    print(v.n[i])
    
    #inpPath=v.makeLayout()
    #v.readLayout(inpPath)
    """
    dot=Digraph(comment='Node Graph',format='plain',engine=None)
    dot.edge_attr.update(arrowhead='none',tailhead='none',dir='none') # forward back both none
    dot.node_attr.update(shape='box')
    dot.node('1','Node1')
    dot.node('2','Node2\nNode4')
    dot.node('3','Node3')
    dot.node('4','Node5 is a \nnode\n bla\nbla\nbla') # Fixed: caveat: cannot use keyword node. replace node by something in postprocessing of input text and replace it back.
    dot.edges(['12','13'])
    dot.edge('3','4')
    print(dot.source)
    dot.render('test-output/firstGraph.gv',view=False)   
    fileObj=open('test-output/firstGraph.gv.plain',mode='r')
    g={}
    n={}
    e={}
    ecnt=0;
    l_prev=''
    nprev=''
    nprevtxt=''
    linestore=''
    dQuote=False
    interdQuoteabsent=False
    qlinecnt=0
    txtLines=[]
    for line in fileObj:
        #print(line)
        a=re.search('"',line)
        #print(a)
        if (not(a==None) or dQuote):
            # if either a quote is present or a quote was found in the previous line capture line.
            dQuote=True
            if dQuote==True and a==None:
                # if there was a quote found before and this line dosent have a quote, make a note of quote absence. when the quote appears again stop capturing (see next if statement).
                interdQuoteabsent=True
            #print(line[:-1] +'---'+line[-1])
            linestore+=line[:-1]+' '
            if (interdQuoteabsent==True and not(a==None)) or (qlinecnt>0 and dQuote==True and  not(a==None)):
                # if there was quote absent in prev line and this line has a quote. this is the end of line capture.
                # or if there were some lines inbetween, after detecting a first quote, check the qlinecnt and a quote was detected previously and if a quote is found in this line stop capture. 
                dQuote=False
                interdQuoteabsent=False
                #print(linestore)
            else:
                qlinecnt+=1
                continue
        if not(linestore==''):
            txtLines.append(linestore)
            linestore=''
            qlinecnt=0
        else:
            txtLines.append(line)

    #print(txtLines)
        
    for line in txtLines:
        l=line.split()
        #print(line)
        l0=l[0]
        if l0=='graph':
                g['scale']=float(l[1])
                g['w']=float(l[2])
                g['h']=float(l[3])
        if l0=='node':
                m=re.search(r'["](.*?)["]',line)
                if m:
                    qtxt=m.group(1)
                    #print(qtxt)
                else:
                    qtxt=l[6]        
                n.update({int(l[1]):{'xy':[float(l[2]),float(l[3])],'w':float(l[4]),'h':float(l[5]),'txt':qtxt, 'style':l[7], 'shape':l[8],'color':l[9],'fillcolor':l[10]}})
        if l0=='edge':
                #print(l)
                e_nn=[]
                e_n=int(l[3])
                delta=range(1,2*e_n)
                dell=[i*2 for i in range(2,e_n+2)]
                for i in range(e_n):
                    #print([i,dell[i],dell[i]+1])
                    e_nn.append([float(l[dell[i]]),float(l[dell[i]+1])])
                    
                e.update({ecnt:{'tail':l[1],'head':l[2],'n':l[3],'pts':e_nn,'labelxy':None,'style':l[4+e_n*2],'color':l[4+(e_n*2)+1]}})
                ecnt+=1
        l_prev=l[0]
    print(g)
    print(n)
    print(e)

    fig, ax=plt.subplots()
    nodeHandle=[]
    #nodeHandle[0]=None
    print(len(n))
    delX=min([n[i]['xy'][0] for i in n])
    delY=min([n[i]['xy'][1] for i in n])
    for i in range(len(n)):
        xcorner=n[i+1]['xy'][0]-n[i+1]['w']*0.5
        ycorner=n[i+1]['xy'][1]-n[i+1]['h']*0.5
        nH=plt.Rectangle((xcorner,ycorner),n[i+1]['w'],n[i+1]['h'])
        #print(i)
        ax.add_patch(nH)
        nodeHandle.append(nH)
    print(str(nodeHandle[0]))
    bleedw=g['scale']*g['w']*0.1
    bleedh=g['scale']*g['h']*0.1
    ax.set_xlim(0-bleedw,g['scale']*g['w']+bleedw)
    ax.set_ylim(0-bleedh,g['scale']*g['h']+bleedh)

    for i in range(len(e)):
        bp=e[i]['pts']
        print(np.array([[i[0] for i in bp],[i[1] for i in bp]]))
        aH=bezierArrow(ax,np.array([[i[0] for i in bp],[i[1] for i in bp]]),arrowDir='end')
   
    fig.tight_layout()
    plt.show()
"""    
    



    """ # Dump
        l0=l[0]
        if l0=='graph':
                g['w']=l[2]
                g['h']=l[3]
        if l0=='node':
                n.update({str(l[1]):{'x':l[2],'y':l[3],'w':l[4],'h':l[5],'txt':l[6]}})
                nprev=str(l[1])
                nprevtxt=l[6]
        if not(l0 in ['node','edge']):
           if l_prev=='node':
               n[nprev].update({'txt':nprevtxt+l[0]})
        l_prev=l[0]

    """
