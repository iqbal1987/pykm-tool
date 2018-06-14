# draggable rectangle with the animation blit techniques; see
# Source: http://www.scipy.org/Cookbook/Matplotlib/Animations
# Thanks to MatplotLib(R) examples
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

class DraggableRectangle:
    lock = None  # only one can be animated at a time
    nheads=None
    ntails=None
    def __init__(self, rect,rID=None,nheads=None,ntails=None,aH=None):
        self.rect = rect
        self.press = None
        self.background = None
        self.ID=rID
        self.nheads=nheads
        self.ntails=ntails
        self.aH=aH
        self.xyFirst=self.rect.xy

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if DraggableRectangle.lock is not None: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata
        DraggableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.rect)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableRectangle.lock is not self:
            return

        self.press = None
        DraggableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None

    # try arrow
        #current xy and center of rectangle
        nx=self.rect.get_xy()
        nw=self.rect.get_width()
        nh=self.rect.get_height()
        nxyabc=(nx[0]+nw/2,nx[1]) #abc=above center
        nxybec=(nx[0]+nw/2,nx[1]+nh) # bec below center
        ncenter=(nx[0]+nw/2,nx[1]+nh/2)
        print(nx)

        # Old xy of rectangle
        ox=self.xyFirst
        oxyabc=(ox[0]+nw/2,ox[1])
        oxybec=(ox[0]+nw/2,ox[1]+nh) # bec below center
        ocenter=(ox[0]+nw/2,ox[1]+nh/2)

        if not(self.ID==None):
            e_id_head=self.nheads[self.ID]
            e_id_tail=self.ntails[self.ID]
            print(self.nheads)
            print(e_id_head)
            print(self.ntails)
            print(e_id_tail)
            print([self.aH[j] for j in e_id_tail])
            print([self.aH[j] for j in e_id_head])
            if not(e_id_head==[]):
                print('Head Exists')
                for j in e_id_head:
                    hxyOld_cp=self.aH[j].n[:,-1]
                    print(self.aH[j].n)
                    self.aH[j].n[0,-1]=nxybec[0]
                    self.aH[j].n[1,-1]=nxybec[1]
                    self.aH[j].bzcalc()
                    print(self.aH[j].ang)
                    print(self.aH[j].arrowDir)
                    self.aH[j].updateArrow()
                #print(hxyOld_cp)
            print(oxyabc)
            print(oxybec)
            print(nxyabc)
            print(nxybec)
            if not(e_id_tail==[]):
                print('Tail Exists')
                for j in e_id_tail:
                    hxyOld_cp=self.aH[j].n[:,-1]
                    print(self.aH[j].n)
                    self.aH[j].n[0,0]=nxyabc[0]
                    self.aH[j].n[1,0]=nxyabc[1]
                    self.aH[j].bzcalc()
                    print(self.aH[j].ang)
                    print(self.aH[j].arrowDir)
                    self.aH[j].updateArrow()

            

        # redraw the full figure
        self.rect.figure.canvas.draw()
        #self.xyFirst=self.rect.xy


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

if __name__=='__main__1':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = ax.bar(range(10), 20*np.random.rand(10))
    drs = []
    for rect in rects:
        dr = DraggableRectangle(rect)
        dr.connect()
        drs.append(dr)

    plt.show()

if __name__=='__main__':
    fig=plt.figure()
    ax=fig.add_subplot(111)
    rects=[None]*2
    rects[0]=ax.add_patch(Rectangle((2,2),5,2))
    rects[1]=ax.add_patch(Rectangle((10,10),5,2,color='red',zorder=-1))
    drs = []
    for rect in rects:
        dr = DraggableRectangle(rect)
        dr.connect()
        drs.append(dr)
    plt.xlim(0,20)
    plt.ylim(0,20)
    plt.show()
