import matplotlib.pyplot as plt
import numpy as np

class Plot:

    def __init__(self, b1, b2):
        fig,axes = plt.subplots(2,2,figsize=(15,10))    # Opens up a figure with four subplots

        total_l = b1.l + b2.l
        data =[]
        
        xlist = [0,b1.x,b2.x]       # Grab the locations of the bobs.
        ylist = [0,b1.y,b2.y]
        
        axes[0,0].plot([-.5,.5],[0,0],'-k',linewidth=5)
        
        line, = axes[0,0].plot(xlist, ylist, '-bo', markersize=10, linewidth=3)

        line1, = axes[0,0].plot(b1.x,b1.y,'-b',linewidth=2)
        line2, = axes[0,0].plot(b2.x,b2.y,'-r',linewidth=2)
        axes[0,0].set_xlim(-total_l,total_l)


        axes[0,0].set_ylim(-total_l,total_l)
        axes[0,0].set_title('t = 0',fontsize=18)
        axes[0,0].set_xlabel('x',fontsize=15)
        axes[0,0].set_ylabel('y',fontsize=15)
        data.append([line,line1,line2])

        line2, = axes[1,0].plot(0,b1.theta,'-b')
        line3, = axes[1,0].plot(0,b2.theta,'-r')
        axes[1,0].set_ylim(-np.pi,np.pi)
        axes[1,0].set_xlabel('t',fontsize=15)
        axes[1,0].set_ylabel('$\\theta$',fontsize=15)
        axes[1,0].set_title("Pendulum angle Vs Time", fontsize=18)
        data.append([line2,line3])

        line1, = axes[0,1].plot(b1.theta,b1.v,'b.')
        
        axes[0,1].set_xlabel('$\\theta$',fontsize=15)
        axes[0,1].set_ylabel('$\\dot{\\theta}$',fontsize=15)
        axes[0,1].set_xlim(-4,4)
        axes[0,1].set_ylim(-6,6)
        axes[0,1].set_title("Phase Diagram", fontsize=20)
        
        line2, = axes[0,1].plot(b2.theta,b2.v,'r.')
        
        axes[1,1].set_xlabel('t',fontsize=15)
        axes[1,1].set_ylabel('Energies',fontsize=15)
        axes[1,1].set_title("System energies Vs Time", fontsize=18)
        
        data.append([line1,line2])
        
        line1, = axes[1,1].plot(0,b1.energy,'-b')
        line2, = axes[1,1].plot(0,b2.energy,'-r')
        line3, = axes[1,1].plot(0,b1.energy+b2.energy,'-m')
        data.append([line1,line2,line3])
        axes[0,0].plot(xlist, ylist,'-o',color='grey',linewidth=3,markersize=10)
        #plt.suptitle("Simulating Double Pendulum", fontsize=25)
        #plt.tight_layout(pad=2)
        
        #plt.show()

        self.fig = fig
        self.axes = axes
        self.data = data


    def update_plots(self, b1,b2,t):
        """ Update all of the plots. """
        self.axes[0,0].set_title('t = %f' % t)
        line,line1,line2 = self.data[0]
        line.set_xdata([0,b1.x,b2.x])
        line.set_ydata([0,b1.y,b2.y])
        line1.set_xdata( np.append(line1.get_xdata(),b1.x))
        line1.set_ydata(np.append(line1.get_ydata(),b1.y))
        line2.set_xdata( np.append(line2.get_xdata(),b2.x))
        line2.set_ydata(np.append(line2.get_ydata(),b2.y))
        
        line1,line2 = self.data[1]
        line1.set_xdata( np.append(line1.get_xdata(), t))
        line1.set_ydata(np.append(line1.get_ydata(),b1.theta))
        line2.set_xdata( np.append(line2.get_xdata(), t))
        line2.set_ydata(np.append(line2.get_ydata(),b2.theta))
        if t > self.axes[1,0].get_xlim()[1]:
            self.axes[1,0].set_xlim(0,t+2)
            
        line1,line2 = self.data[2]
        line1.set_xdata( np.append(line1.get_xdata(), b1.theta))
        line1.set_ydata(np.append(line1.get_ydata(),b1.v))
        line2.set_xdata( np.append(line2.get_xdata(), b2.theta))
        line2.set_ydata(np.append(line2.get_ydata(),b2.v))
        
        line1,line2,line3 = self.data[3]
        line1.set_xdata( np.append(line1.get_xdata(), t))
        line1.set_ydata(np.append(line1.get_ydata(),b1.energy))
        line2.set_xdata( np.append(line2.get_xdata(), t))
        line2.set_ydata(np.append(line2.get_ydata(),b2.energy))
        line3.set_xdata( np.append(line3.get_xdata(), t))
        line3.set_ydata(np.append(line3.get_ydata(),b1.energy+b2.energy))
        if t > self.axes[1,1].get_xlim()[1]:
            self.axes[1,1].set_xlim(0,t+2)
                        
        plt.pause(1e-10)
        #plt.show()
