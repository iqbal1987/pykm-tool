# Use Graphviz layout engine
import re
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
class VisualizeOnto:
       dotFile=None
       def __init__(self):
            self.dotFile=[]
       def makeLayout(self):
            # call GV layout with the content of the grapgh
            textfilepath=''
            return textfilepath
            
        
       def readLayout(self,inpPath):
            pass

if __name__=="__main__":
    v=VisualizeOnto()
    inpPath=v.makeLayout()
    v.readLayout(inpPath)
    dot=Digraph(comment='Node Graph',format='plain',engine=None)
    dot.node('1','Node1')
    dot.node('2','Node2\nNode4')
    dot.node('3','Node3')
    dot.edges(['12','13'])
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
                print(l)
                e_nn=[]
                e_n=int(l[3])
                delta=range(1,2*e_n)
                dell=[i*2 for i in range(2,e_n+2)]
                for i in range(e_n):
                    #print([i,dell[i],dell[i]+1])
                    e_nn.append([l[dell[i]],l[dell[i]+1]])
                    
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
    for i in range(len(n)):
        nH=plt.Rectangle(n[i+1]['xy'],n[i+1]['w'],n[i+1]['h'])
        #print(i)
        ax.add_patch(nH)
        nodeHandle.append(nH)
    print(str(nodeHandle[0])) 
    ax.set_xlim(0,2*g['scale']*g['w'])
    ax.set_ylim(0,2*g['scale']*g['h'])
    fig.tight_layout()
    plt.show()
    
    



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
