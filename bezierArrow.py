import bezier
import numpy as np
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class bezierArrow:
    bcPointsXY=None
    arrowDir='start'
    num_pts=100
    ax=None
    def __init__(self,ax,bcPointsXY=None,arrowDir='start',num_pts=100):
        self.xy=bcPointsXY
        self.arrowDir=arrowDir
        self.num_pts=num_pts
        self.ax=ax
        self.bzcalc(True)

    def bzcalc(self,addBool=False):
        self.n=self.xy #np.asfortranarray([self.xy[0,:],self.xy[1,:],])
        self.c=bezier.Curve(self.n,degree=2)
        p=self.c.evaluate_multi(np.linspace(0.0,1.0,self.num_pts))
        npts=5
        if self.arrowDir=='start':
            ang=np.arctan2((p[1,npts]-p[1,0]),(p[0,npts]-p[0,0]))*180/np.pi
            self.tip=(p[0,0],p[1,0])
        elif self.arrowDir=='end':
            ang=np.arctan2((p[1,-npts]-p[1,-1]),(p[0,-npts]-p[0,-1]))*180/np.pi
            self.tip=(p[0,-1],p[1,-1])
        else:
            ang=0
            self.tip=(0,0)
            
        self.ang=ang
        self.radiusArrowHead=self.c.length*0.2
        self.p=p
        
        if addBool:
            self.addToAxes()
        
    def addToAxes(self):
        self.aHead=self.ax.add_patch(Wedge(self.tip, self.radiusArrowHead, self.ang-5,self.ang+5,transform=self.ax.transData, color='k'))
        self.aLine=self.ax.add_line(Line2D(self.p[0,:],self.p[1,:], linewidth=1, linestyle='-', color='k'))

    def updateArrow(self):
        self.aHead.set_center(self.tip)
        self.aHead.set_theta1(self.ang-5)
        self.aHead.set_theta2(self.ang+5)
        self.aLine.set_xdata(self.p[0,:])
        self.aLine.set_ydata(self.p[1,:])
                         
if __name__=="__main__":
    fig=plt.figure()
    ax=fig.add_subplot(111)
    bz=bezierArrow(ax,np.array([[0.0,10.0,100],[0.0,50.0,100]]))
    print(bz.aHead)
    print(bz.aLine)
    #print(ax)
    #print(dir(ax))
    ax.add_artist(bz.aHead)
    ax.add_line(bz.aLine)
    ax.relim()
    ax.autoscale()
    ax.set_xlim([0,160])
    ax.set_ylim([0,160])
    j=0
    ax.text(10,10,str(j))
    plt.show()
    for i in range(1000000):
        j=j+1
    bz.aHead.set_center((10,10))
    plt.show()
    
